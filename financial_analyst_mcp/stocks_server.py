from typing import Any
from mcp.server.fastmcp import FastMCP
import yfinance as yf
import json
from dotenv import load_dotenv
import sys
import logging

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

mcp = FastMCP("Stocks")

def get_company_info(ticker: str) -> dict[str, Any] | None:
    """
    Get company information for a given stock ticker.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple Inc.).
    
    Returns:
        dict: Company information or None if the ticker is invalid.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info
    except Exception as e:
        logger.error(f"Error fetching company info for {ticker}: {e}")
        return None
    
@mcp.tool()
def get_company_details(ticker: str) -> str:
    """
    Get company details for a given stock ticker.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple Inc.).
    
    Returns:
        str: Formatted string of company details or an error message if the ticker is invalid.
    """
    company_info = get_company_info(ticker)
    
    if not company_info or "country" not in company_info:
        return f"Unable to fetch details for ticker: {ticker}"
    
    return json.dumps(company_info, indent=4)

@mcp.tool()
def get_company_prices(ticker: str,period='1mo') -> str:
    """
    Get stock prices for a given ticker.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple Inc.).
    
    Returns:
        str: Formatted string of stock prices or an error message if the ticker is invalid.
    """
    try:
        stock = yf.Ticker(ticker)
        price_history = stock.history(period=period)
    except Exception as e:
        logger.error(f"Error fetching stock prices for {ticker}: {e}")
        return f"Unable to fetch prices for ticker: {ticker}"
    
    return json.dumps(price_history.to_dict(orient='records'), indent=4,default=str)    

@mcp.resource("companies://")
def get_company_tickers_all() -> str:
    """
    Get a list of company tickers.
    
    Returns:
        str: JSON string of company tickers.
    """
    try:
        with open("tickers.json", "r") as file:
            tickers = json.load(file)
        return json.dumps(tickers, indent=4)
    except FileNotFoundError:
        return "Tickers file not found."
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from tickers file: {e}")
        return "Error reading tickers data."

# Add a dynamic company ticker resource    
@mcp.resource("company://{ticker}")
def get_company_ticker(ticker: str) -> str:
    """
    Get company details for a specific ticker.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple Inc.).
    
    Returns:
        str: JSON string of company details or an error message if the ticker is invalid.
    """
    with open("tickers.json", "r") as file:
        try:
            tickers = json.load(file)
            company_ticker = [t for t in tickers if t["ticker"].upper() == ticker.upper()]
            return json.dumps(company_ticker[0], indent=4) if company_ticker else f"No details found for ticker: {ticker}"
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from tickers file: {e}")
            return "Error reading tickers data."

@mcp.prompt()
def analyze_company_stock(ticker: str) -> str:
    """
    Analyze a company's stock based on its ticker.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple Inc.).
    
    Returns:
        str: Analysis of the company's stock.
    """
    pormpt =   f"""Analyze the stock of the company with ticker {ticker}.
    Provide insights on its performance, market trends, and any relevant news.
    Use stock prices for last 3 months.
    Use the company details and stock prices to support your analysis."""

    return pormpt

if __name__ == "__main__":
    # Initialize and run MCP server
    mcp.run(transport="stdio")