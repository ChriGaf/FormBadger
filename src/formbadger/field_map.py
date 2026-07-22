from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class FieldMap:
    page: int
    field_name: str
    value: str
