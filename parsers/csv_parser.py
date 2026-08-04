import csv
import io
from typing import TYPE_CHECKING, BinaryIO

from models.dataclasses.raw_transaction import RawTransaction
from parsers.abc_parser import ABCParser

if TYPE_CHECKING:
    from collections.abc import Iterator


class CSVParser(ABCParser):
    """Parser to parse CSV files."""

    def __init__(self, file: BinaryIO) -> None:
        self._file = file

    def parse(self) -> Iterator[RawTransaction]:
        """Parse a raw CSV file and yield each row."""
        reader = csv.DictReader(io.TextIOWrapper(self._file, encoding="utf-8"))

        for row in reader:
            yield RawTransaction(values=row)
