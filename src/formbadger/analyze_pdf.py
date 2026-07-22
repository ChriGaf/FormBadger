from pathlib import Path

from pypdf import PdfReader

from formbadger import field_map_csv
from formbadger.field_map import FieldMap

# TODO: use logger


def extract_field_map(
    pdf_field,
    page: int,
) -> FieldMap | None:
    """Extract a supported form field from a PDF widget."""
    field_name = pdf_field.get("/T", "")
    field_type = pdf_field.get("/FT", "")
    field_value = pdf_field.get("/V", "")

    # skip any field if either the name of field type is incomplete
    # actually I am not sure if this can happen, but this is a bit defensive programming
    if not field_name or not field_type:
        print(f"Skipping incomplete field '{field_name}' on page '{page}' with type '{field_type}'")
        return None

    # for now, we only encountered "text", which is encoded as "/Tx"
    if field_type != "/Tx":
        # let's just warn for now and skip it...
        print(f"Skipping field '{field_name}' on page {page} because of unknown type: '{field_type}'")
        return None

    # warn if a field has no value; this may be hard to match with trial and error
    if not field_value:
        print(
            f"Note that field '{field_name}' on page '{page}' with type '{field_type}' "
            "has no value and may be hard to match manually"
        )

    return FieldMap(
        page=page,
        field_name=field_name,
        value=field_value,
    )


def resolve_pdf_field(widget):
    """Return the actual field object, following /Parent if necessary."""
    # AI: some pdfs store name/value in parent, so apparently we prefer that
    if "/Parent" in widget:
        return widget["/Parent"].get_object()
    return widget


def analyze_template(
    template_file: Path,
) -> list[FieldMap]:
    """Extract all supported form fields from a PDF template."""
    pdf_reader = PdfReader(template_file)

    field_maps = []

    for page_no, page in enumerate(pdf_reader.pages, start=1):
        page_annotations = page.get("/Annots")
        if page_annotations is None:
            continue

        for annotation in page_annotations:
            field_map = extract_field_map(
                resolve_pdf_field(annotation.get_object()),
                page_no,
            )
            if field_map is not None:
                field_maps.append(field_map)

    return field_maps


def analyze_templates(templates_folder: Path) -> None:
    """Analyze all PDF templates in a directory."""
    template_files = list(templates_folder.glob("*.pdf"))

    # iterate over all .pdf files in template folder
    for pdf_file in template_files:
        # output .csv file is saved beside the template file
        csv_file = templates_folder / f"{pdf_file.stem}.csv"

        if csv_file.exists():
            # skip if it already exists
            print(f"Skipping template file '{pdf_file.name}' because the field-map .csv already exists")
            continue

        field_maps = analyze_template(pdf_file)
        field_map_csv.write(field_maps, csv_file)


def main() -> None:
    # TODO: write actual CLI
    pdf_template_folder = Path("templates")

    analyze_templates(pdf_template_folder)


if __name__ == "__main__":
    main()
