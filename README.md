# MCP Demo Project

A demonstration project showcasing Model Context Protocol (MCP) integration with weather and stock market data services.

## Features

- **Weather Service**
  - Get weather alerts for any US state
  - Get weather forecasts based on latitude and longitude
  - Uses the National Weather Service (NWS) API

- **Stock Market Service**
  - Get detailed company information for any stock ticker
  - Retrieve stock price data with customizable time periods
  - Powered by Yahoo Finance API

## Requirements

- Python 3.11 or higher
- Dependencies listed in `pyproject.toml`:
  - `mcp[cli]>=1.13.0` - Model Context Protocol framework
  - `httpx>=0.28.1` - Asynchronous HTTP client
  - `yfinance>=0.2.65` - Yahoo Finance API client
  - `matplotlib>=3.10.5` - Data visualization
  - `duckduckgo-search>=8.1.1` - Search functionality
  - `ddgs>=9.5.4` - DuckDuckGo search utilities

## Installation

1. Clone the repository
2. Create and activate a Python virtual environment
3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### Weather Service

```python
# Get weather alerts for California
await get_alerts("CA")

# Get weather forecast for a location
await get_forecast(37.7749, -122.4194)  # San Francisco coordinates
```

### Stock Market Service

```python
# Get company details
get_company_details("AAPL")  # Get Apple Inc. details

# Get stock prices
get_company_prices("MSFT", period="1mo")  # Get Microsoft's monthly stock prices
```

## Project Structure

- `weather.py` - Weather service implementation using NWS API
- `stocks.py` - Stock market service using Yahoo Finance
- `pyproject.toml` - Project dependencies and metadata

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
