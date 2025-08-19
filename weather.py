from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import yfinance as yf
import json

mcp = FastMCP("weather")

NEW_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str,Any] | None:
    """"
    Make a request to the NWS API with proper error handling.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }
    

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            mcp.logger.error(f"Error fetching data from NWS API: {e}")
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    properties = feature.get("properties", {})
    return f"""
Event : {properties.get("event", "Unknown Event")}
Area: {properties.get("areaDesc", "No area description available")}
Severity: {properties.get("severity", "Unknown Severity")}
Description: {properties.get("description", "No description available")}
Instructions: {properties.get("instruction", "No specific instructions available")}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Get weather alerts for a US state
    
    Args:
        state (str): The two-letter state code (e.g., 'CA' for California).
    
    Returns:
        str: Formatted string of weather alerts or a message if no alerts are found.
    """
    url = f"{NEW_API_BASE}/alerts/active?area={state}"
    data = await make_nws_request(url)
    
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
        return f"No active weather alerts found for {state}."
    if not data["features"]:
        return f"No active weather alerts found for {state}."
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Get the weather forecast for a location.
    
    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
    
    Returns:
        str: Formatted string of the weather forecast or an error message.
    """
    points_url = f"{NEW_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)
    
    if not points_data:
        return "Unable to fetch forecast data for this location."
    
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)
    if not forecast_data:
        return "Unable to fetch detailed forecast data for this location."
    
    periods = forecast_data["properties"].get("periods", [])
    forecasts = []

    if not periods:
        return "No forecast data available for the specified location."
    
    for period in periods[:5]:
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast.strip())
    return "\n---\n".join(forecasts)


if __name__ == "__main__":
    # Initialize and run MCP server
    mcp.run(transport="stdio")