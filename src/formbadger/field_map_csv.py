import csv
from pathlib import Path

from formbadger.constants import (
    CSV_DELIMITER,
    CSV_ENCODING,
    FIELD_NAME,
    PAGE,
    VALUE,
)
from formbadger.field_map import FieldMap


def read(path: Path) -> list[FieldMap]:
    """Read field definitions from a CSV file."""
    with path.open("r", encoding=CSV_ENCODING) as csv_file:
        csv_reader = csv.DictReader(
            csv_file,
            delimiter=CSV_DELIMITER,
        )

        return [
            FieldMap(
                page=int(row[PAGE].strip()),
                field_name=row[FIELD_NAME].strip(),
                value=row[VALUE].strip(),
            )
            for row in csv_reader
        ]


def write(field_maps: list[FieldMap], path: Path) -> None:
    """Write field definitions to a CSV file."""
    with path.open("w", newline="", encoding=CSV_ENCODING) as csv_file:
        csv_writer = csv.DictWriter(
            csv_file,
            fieldnames=[PAGE, FIELD_NAME, VALUE],
            delimiter=CSV_DELIMITER,
        )

        csv_writer.writeheader()

        for field_map in field_maps:
            csv_writer.writerow(
                {
                    PAGE: field_map.page,
                    FIELD_NAME: field_map.field_name,
                    VALUE: field_map.value,
                }
            )
