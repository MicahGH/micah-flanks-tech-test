from abc import ABC, abstractmethod
from collections.abc import Iterator

from models.dataclasses.raw_transaction import RawTransaction


class ABCParser(ABC):
    """An abstract base class for all parsers."""

    @abstractmethod
    def parse(self) -> Iterator[RawTransaction]:
        """Parse method which is obligatory for subclasses to implement."""
        raise NotImplementedError
