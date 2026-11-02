from decimal import Decimal

from mcp.server.fastmcp import FastMCP

from mcp_servers.finance_server.tools import (
    convert_currency as conversion_logic,
    get_exchange_rate as rate_logic,
)


mcp = FastMCP(
    "FinanceMCPServer",
    host="127.0.0.1",
    port=8002
)


@mcp.tool()
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str
) -> dict:
    """
    Convert an amount between supported currencies.

    Example:
    Convert 100 USD into INR.
    """

    return conversion_logic(
        amount=Decimal(str(amount)),
        from_currency=from_currency,
        to_currency=to_currency
    )


@mcp.tool()
def get_exchange_rate(
    from_currency: str,
    to_currency: str
) -> dict:
    """
    Get exchange rate between two currencies.

    Example:
    Get USD to INR exchange rate.
    """

    return rate_logic(
        from_currency,
        to_currency
    )


if __name__ == "__main__":

    print("Starting Finance MCP Server...")
    print("Server URL: http://127.0.0.1:8002/mcp")

    mcp.run(transport="streamable-http")