# MCP Project

A comprehensive demonstration project showcasing Model Context Protocol (MCP) integration with AI-powered applications, featuring weather and stock market data services.

## Overview

This project demonstrates multiple approaches to integrating MCP servers with language models:
- **FastMCP Server** - Building custom MCP servers with async tools
- **OpenAI Function Calling** - Direct integration with OpenAI's function calling API
- **MCP Client** - Connecting to MCP servers programmatically

## Features

### Weather Service
- Get real-time weather alerts for any US state
- Retrieve detailed weather forecasts based on latitude and longitude
- Uses the National Weather Service (NWS) API
- Async/await support for efficient I/O

### Stock Market Service
- Retrieve detailed company information for any stock ticker
- Get historical and current stock price data with customizable time periods
- Access company financials, market cap, P/E ratios, and more
- Powered by Yahoo Finance API
- Price comparison and analysis tools

### Data Analysis & Visualization
- Generate price comparison charts for multiple stocks
- Analyze 3-month price trends
- Performance metrics and statistical analysis
- Matplotlib-based visualization with multiple chart types

## Project Structure

```
mcpdemo/
├── my_first_mcp_server/          # FastMCP server implementation
│   ├── weather_server.py         # MCP server with weather tools
│   └── weather_client.py         # Client for testing the server
├── function_calling/              # OpenAI function calling examples
│   └── weather.py                # Weather service with OpenAI integration
├── financial_analyst_mcp/        # Financial analysis MCP server
├── weather.py                    # Standalone weather service
├── stocks.py                     # Standalone stock market service
├── process_tickers.py            # Ticker data processing utility
├── price_comparison.py           # Stock price comparison and charting
├── pyproject.toml                # Project dependencies and configuration
├── package.json                  # Node.js dependencies
├── workshop.md                   # Workshop documentation and examples
└── README.md                     # This file
```

## Requirements

- Python 3.11 or higher
- Dependencies listed in `pyproject.toml`:
  - `mcp[cli]>=1.13.0` - Model Context Protocol framework
  - `fastmcp>=2.14.3` - FastMCP server framework for building MCP servers
  - `httpx>=0.28.1` - Asynchronous HTTP client
  - `yfinance>=0.2.65` - Yahoo Finance API client
  - `matplotlib>=3.10.5` - Data visualization
  - `openai>=2.15.0` - OpenAI API client
  - `mcp-openai[cli]>=0.2.0` - MCP and OpenAI integration
  - `langchain-mcp-adapters>=0.2.1` - LangChain MCP adapters
  - `duckduckgo-search>=8.1.1` - DuckDuckGo search functionality
  - `ddgs>=9.5.4` - DuckDuckGo search API utilities
  - `duckdb>=1.4.3` - DuckDB SQL engine for data processing

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcpdemo
   ```

2. Create and activate a Python virtual environment:
   ```bash
   uv sync
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Set up environment variables:
   ```bash
   touch .env
   # Edit .env with your API keys (OpenAI, etc.)
   ```

## Usage

### Running the FastMCP Weather Server

```bash
cd my_first_mcp_server
uv run python weather_server.py
```

### Testing the Weather Client

```bash
cd my_first_mcp_server
uv run python weather_client.py
```

### OpenAI Function Calling Example

```bash
cd function_calling
uv run python weather.py
```

### Stock Price Analysis

```bash
# Get company details and prices
uv run python -c "from stocks import get_company_details; print(get_company_details('AAPL'))"

# Generate price comparison chart
uv run python price_comparison.py
```

### Using Standalone Services

```python
# Weather Service
from weather import get_alerts, get_forecast

# Get alerts for California
alerts = await get_alerts("CA")

# Get forecast for San Francisco
forecast = await get_forecast(37.7749, -122.4194)

# Stock Service
from stocks import get_company_details, get_company_prices

# Get Apple's information
details = get_company_details("AAPL")

# Get Microsoft's 3-month price history
prices = get_company_prices("MSFT", period="3mo")
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Key Components

### weather_server.py
FastMCP-based weather service providing:
- `get_alerts(state)` - Weather alerts for US states
- `get_forecast(latitude, longitude)` - Weather forecasts

### stocks.py
Yahoo Finance integration providing:
- `get_company_details(ticker)` - Detailed company information
- `get_company_prices(ticker, period)` - Historical price data

### price_comparison.py
Data analysis tool generating:
- Normalized price comparison charts
- Actual price comparison with dual axes
- Performance metrics and statistics


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## References

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [National Weather Service API](https://www.weather.gov/documentation/services-web-api)
- [Yahoo Finance API (yfinance)](https://github.com/ranaroussi/yfinance)
