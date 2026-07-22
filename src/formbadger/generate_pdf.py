import csv
import shutil
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from formbadger import field_map_csv
from formbadger.constants import (
    CSV_DELIMITER,
    CSV_ENCODING,
    OUTPUT_FILENAME_FIELD,
)
from formbadger.field_map import FieldMap
from formbadger.utils import sanitize_names

PageMappings = dict[int, dict[str, str]]


def create_page_field_mappings(
    field_maps: list[FieldMap],
) -> PageMappings:
    page_mappings: PageMappings = {}

    for field_map in field_maps:
        page_mapping = page_mappings.setdefault(field_map.page, {})
        page_mapping[field_map.value] = field_map.field_name

    return page_mappings


def create_pdf_fields(
    page_field_mapping: dict[str, str],
    row: dict[str, str],
) -> dict[str, str]:
    return {field: row[csv_column] for csv_column, field in page_field_mapping.items()}


def generate_pdf(
    template_file: Path,
    page_field_mappings: PageMappings,
    output: Path,
    row: dict[str, str],
) -> None:
    pdf = PdfReader(template_file)
    pdf_writer = PdfWriter()
    pdf_writer.append(pdf)  #

    for page_no, page in enumerate(pdf_writer.pages, start=1):
        if page_no not in page_field_mappings:
            print(f"Skipping page {page_no}: no field mappings defined.")
            continue

        try:
            fields = create_pdf_fields(page_field_mappings[page_no], row)
        except KeyError as e:
            print(f"Skipping page {page_no}: missing input column '{e}'.")
            continue
        pdf_writer.update_page_form_field_values(page, fields)

    pdf_writer.set_need_appearances_writer()

    with output.open("wb") as output_file:
        pdf_writer.write(output_file)


def generate_pdfs(template_file: Path, data_file: Path, output_dir: Path) -> None:
    # load the field-map file
    field_maps_file = template_file.with_suffix(".csv")
    if not field_maps_file.is_file():
        print("Field map file not found:", field_maps_file)
        return

    field_maps = field_map_csv.read(field_maps_file)
    page_mappings = create_page_field_mappings(field_maps)

    with data_file.open(encoding=CSV_ENCODING) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=CSV_DELIMITER)

        # validate the required column exists
        if OUTPUT_FILENAME_FIELD not in csv_reader.fieldnames:
            print(
                f"The input CSV must contain a column named '{OUTPUT_FILENAME_FIELD}', "
                "which is used to generate the output filenames.",
                file=sys.stderr,
            )
            return

        for row in csv_reader:
            data_id = sanitize_names(row[OUTPUT_FILENAME_FIELD])
            output_file = output_dir / f"{data_file.stem}_{data_id}.pdf"

            generate_pdf(template_file, page_mappings, output_file, row)


def main() -> None:
    # TODO: write actual CLI
    input_data = Path("input/Teilnehmer_2026.csv")
    input_template = Path("templates/Vorlage Teilnahmebestätigung (ausfüllbar).pdf")
    output = Path("output")

    if not input_template.is_file():
        print(f"Input file '{input_template}' not found", file=sys.stderr)
        sys.exit(1)
    if not input_data.is_file():
        print(f"Input file '{input_data}' not found", file=sys.stderr)
        sys.exit(1)

    # this is mostly a matter of preference
    # I like to name the output directory after the input file
    # and include copies of both the template and the input file
    output_dir = Path(output) / input_data.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(input_data, output_dir / input_data.name)
    shutil.copy2(input_template, output_dir / input_template.name)

    generate_pdfs(input_template, input_data, output_dir)


if __name__ == "__main__":
    main()
