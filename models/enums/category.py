from enum import StrEnum


class Category(StrEnum):
    """Supported transaction categories."""

    TRANSPORTE = "TRANSPORTE"
    EDUCACION = "EDUCACION"
    RESTAURANTES = "RESTAURANTES"
    SUPERMERCADOS = "SUPERMERCADOS"
    OCIO = "OCIO"
    SALUD = "SALUD"
    HOGAR = "HOGAR"
    VIAJES = "VIAJES"
    NOMINA = "NOMINA"
    TRANSFERENCIAS = "TRANSFERENCIAS"
    OTROS = "OTROS"

    @classmethod
    def from_raw(cls, value: str) -> Category:
        """Convert raw to enum."""
        normalized = value.strip().upper()

        try:
            return cls(normalized)
        except ValueError as exc:
            msg = f"Unsupported category: {value}"
            raise ValueError(msg) from exc
