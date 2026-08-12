from dataclasses import dataclass


@dataclass
class ImportResult:
    """Dataclass for the results of an import."""

    total: int = 0
    imported: int = 0
    updated: int = 0
    malformed: int = 0
