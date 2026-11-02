from mcp_servers.database_server.database import (
    initialize_database
)

from mcp_servers.database_server.tools import (
    search_customers,
    get_customer
)


def setup_module():
    initialize_database()


def test_search_customers():

    result = search_customers(
        query="Rahul"
    )

    assert result["success"] is True
    assert result["count"] >= 1


def test_search_by_city():

    result = search_customers(
        query="Ludhiana"
    )

    assert result["success"] is True
    assert result["count"] >= 1


def test_get_customer():

    result = get_customer(
        customer_id=1
    )

    assert result["success"] is True
    assert result["customer"]["id"] == 1


def test_customer_not_found():

    result = get_customer(
        customer_id=999999
    )

    assert result["success"] is False
    assert result["error"] == "CUSTOMER_NOT_FOUND"