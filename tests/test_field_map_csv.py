from pathlib import Path

from formbadger import field_map_csv
from formbadger.constants import FIELD_NAME, PAGE, VALUE
from formbadger.field_map import FieldMap


def test_read(tmp_path: Path) -> None:
    csv_file = tmp_path / "field_map.csv"

    csv_file.write_text(
        (f"{PAGE};{FIELD_NAME};{VALUE}\n" "1;First Name;firstname\n" "2;Last Name;lastname\n"),
        encoding="utf-8",
    )

    assert field_map_csv.read(csv_file) == [
        FieldMap(page=1, field_name="First Name", value="firstname"),
        FieldMap(page=2, field_name="Last Name", value="lastname"),
    ]


def test_write(tmp_path: Path) -> None:
    csv_file = tmp_path / "field_map.csv"

    field_map_csv.write(
        [
            FieldMap(page=1, field_name="First Name", value="firstname"),
            FieldMap(page=2, field_name="Last Name", value="lastname"),
        ],
        csv_file,
    )

    assert (
        csv_file.read_text(encoding="utf-8") == f"{PAGE};{FIELD_NAME};{VALUE}\n"
        "1;First Name;firstname\n"
        "2;Last Name;lastname\n"
    )


def test_round_trip(tmp_path: Path) -> None:
    csv_file = tmp_path / "field_map.csv"

    expected = [
        FieldMap(page=1, field_name="First Name", value="firstname"),
        FieldMap(page=2, field_name="Last Name", value="lastname"),
    ]

    field_map_csv.write(expected, csv_file)

    assert field_map_csv.read(csv_file) == expected
