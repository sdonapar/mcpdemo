import sys
from typing import Any
from openai import OpenAI
import json
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logger
logging.basicConfig(
    level=logging.INFO, # Set the minimum logging level to output (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

client = OpenAI()

NSW_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

def make_nws_request(url: str) -> dict[str,Any] | None:
    """"
    Make a request to the NWS API with proper error handling.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json",
    }

    with httpx.Client() as client:
        try:
            response = client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching data from NWS API: {e}")
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

# 1. Define a list of callable tools for the model
tools = [
    {
        "type": "function",
        "name": "get_alerts",
        "description": "Get weather alerts for a US state",
        "parameters": {
            "type": "object",
            "properties": {
                "state": {
                    "type": "string",
                    "description": "The two-letter state code (e.g., 'CA' for California).",
                },
            },
            "required": ["state"],
        },
    },
    {
        "type": "function",
        "name": "get_forecast",
        "description": "Get the weather forecast for a location.",
        "parameters": { 
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "Latitude of the location.",
                },
                "longitude": {
                    "type": "number",
                    "description": "Longitude of the location.",
                },
            },
            "required": ["latitude", "longitude"],
        },
    },
]

def get_alerts(state: str) -> str:
    """
    Get weather alerts for a US state
    
    Args:
        state (str): The two-letter state code (e.g., 'CA' for California).
    
    Returns:
        str: Formatted string of weather alerts or a message if no alerts are found.
    """
    url = f"{NSW_API_BASE}/alerts/active?area={state}"
    data =  make_nws_request(url)
    
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
        return f"No active weather alerts found for {state}."
    if not data["features"]:
        return f"No active weather alerts found for {state}."
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

def get_forecast(latitude: float, longitude: float) -> str:
    """
    Get the weather forecast for a location.
    
    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
    
    Returns:
        str: Formatted string of the weather forecast or an error message.
    """
    points_url = f"{NSW_API_BASE}/points/{latitude},{longitude}"
    points_data =  make_nws_request(points_url)
    
    if not points_data:
        return "Unable to fetch forecast data for this location."
    
    forecast_url = points_data["properties"]["forecast"]
    forecast_data =  make_nws_request(forecast_url)
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

input_list = [
    {"role": "user", "content": "What is weather forecast in Dallas, TX?"}
]

# 2. Prompt the model with tools defined
response = client.responses.create(
    model="gpt-4o-mini",
    tools=tools,
    input=input_list,
)

# Save function call outputs for subsequent requests
input_list += response.output

for item in response.output:
    if item.type == "function_call":
        if item.name == "get_alerts":
            # 3. Execute the function logic for get_horoscope
            alerts = get_alerts(json.loads(item.arguments))
            
            # 4. Provide function call results to the model
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({
                  "alerts": alerts
                })
            })
        if item.name == "get_forecast":
            # 3. Execute the function logic for get_forecast
            forecast = get_forecast(
                json.loads(item.arguments)['latitude'],
                json.loads(item.arguments)['longitude']
            )
            
            # 4. Provide function call results to the model
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({
                  "forecast": forecast
                })
            })

logger.debug("Input list for final response:")
logger.debug(json.dumps(input_list, indent=2, default=str))


response = client.responses.create(
    model="gpt-4o-mini",
    instructions="Respond only with weather information generated by tool.",
    tools=tools,
    input=input_list,
)

# 5. The model should be able to give a response!
logger.info("Final output:")
logger.info(response.model_dump_json(indent=2))
logger.info(f"\n{response.output_text}")