from mcp.server.fastmcp import FastMCP

from mcp_servers.weather_server.tools import (
    get_weather as weather_logic,
    get_forecast as forecast_logic
)


# Initialize MCP server
mcp = FastMCP(
    "WeatherMCPServer",
    host="0.0.0.0",
    port=8001
)


@mcp.tool()
def get_weather(city: str) -> dict:
    """
    Get current mock weather information
    for a specified city.
    """
    return weather_logic(city)


@mcp.tool()
def get_forecast(city: str, days: int = 3) -> dict:
    """
    Get mock weather forecast for a city.
    Supports forecasts between 1 and 7 days.
    """
    return forecast_logic(city, days)


if __name__ == "__main__":
    print("Starting Weather MCP Server...")
    print("MCP endpoint: http://localhost:8001/mcp")

    mcp.run(transport="streamable-http")