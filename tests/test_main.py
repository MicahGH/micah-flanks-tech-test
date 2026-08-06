from http.client import OK

from fastapi.testclient import TestClient
from httpx import Response


def test_get_transactions(client: TestClient) -> None:
    """Test get_transactions() endpoint."""
    response: Response = client.get(  # type: ignore[reportUnknownMemberType]
        url="/transactions",
        params={
            "account_id": 1,
            "from_date": "2024-01-01",
            "to_date": "2024-12-31",
        },
    )

    assert response.status_code == OK  # type: ignore[reportUnknownMemberType]

    assert isinstance(
        response.json(),  # type: ignore[reportUnknownMemberType]
        list,
    )


def test_get_transaction_summary(client: TestClient) -> None:
    """Test get_transaction_summary() endpoint."""
    response: Response = client.get(  # type: ignore[reportUnknownMemberType]
        url="/transactions/summary",
        params={
            "account_id": 1,
        },
    )

    assert response.status_code == OK  # type: ignore[reportUnknownMemberType]

    data = response.json()  # type: ignore[reportUnknownMemberType]

    assert "total_balance" in data
    assert "total_credits" in data
    assert "total_debits" in data
