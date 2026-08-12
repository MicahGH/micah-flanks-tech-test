from enum import StrEnum


class UpsertResult(StrEnum):
    """Results from an UPSERT."""

    INSERTED = "inserted"
    UPDATED = "updated"
