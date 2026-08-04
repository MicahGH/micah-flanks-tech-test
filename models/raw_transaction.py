from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RawTransaction:
    """Dataclass to represent a raw transaction."""

    values: dict[str, str]
