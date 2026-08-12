from models.postgres.malformed_transaction import MalformedTransaction
from repositories.base_repository import BaseRepository


class MalformedTransactionRepository(BaseRepository[MalformedTransaction]):
    """Repository for the malformed_transaction table."""
