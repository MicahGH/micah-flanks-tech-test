from pathlib import Path
from typing import TYPE_CHECKING

from parsers.csv_parser import CSVParser

if TYPE_CHECKING:
    from fastapi import UploadFile

    from parsers.abc_parser import ABCParser


class UnsupportedFileTypeError(BaseException):
    """Raised when no suitable parser is found for the file type."""


class ParserFactory:
    """Factory to create the relevant parser for the file provided."""

    @staticmethod
    def create(upload_file: UploadFile) -> ABCParser:
        """Create the relevant parser for the file."""
        suffix = Path(upload_file.filename or "").suffix.lower()

        match suffix:
            case ".csv":
                return CSVParser(upload_file.file)
            case _:
                raise UnsupportedFileTypeError(suffix)
