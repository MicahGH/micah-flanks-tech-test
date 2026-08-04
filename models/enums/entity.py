from enum import StrEnum


class Entity(StrEnum):
    """Supported banking entities."""

    SANTANDER = "santander"
    SABADELL = "sabadell"
    LACAIXA = "lacaixa"
