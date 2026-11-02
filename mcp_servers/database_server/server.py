from mcp.server.fastmcp import FastMCP

from mcp_servers.database_server.database import (
    initialize_database
)

from mcp_servers.database_server.tools import (
    search_customers as search_logic,
    get_customer as get_customer_logic
)


mcp = FastMCP(
    "DatabaseMCPServer",
    host="127.0.0.1",
    port=8003
)


@mcp.tool()
def search_customers(
    query: str,
    limit: int = 10
) -> dict:
    """
    Search customers by name, email, or city.

    Example: Find customers in Ludhiana.
    """

    return search_logic(
        query=query,
        limit=limit
    )


@mcp.tool()
def get_customer(customer_id: int) -> dict:
    """
    Retrieve a customer using their database ID.

    Example: Get customer with ID 1.
    """

    return get_customer_logic(customer_id)


if __name__ == "__main__":

    initialize_database()

    print("Starting Database MCP Server...")
    print("Server URL: http://127.0.0.1:8003/mcp")

    mcp.run(transport="streamable-http")