import json
import re
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

tickers = []
unique_ticers = []
with open("tickers.txt", "r") as file:
    for line in file:
        try:
            ticker,name,sector,mcap = line.strip().split("\t",3)
            # name,mcap = rest.rsplit("\t", 1)
            # re.sub("\t+"," ", name)  # Clean up any extra tabs
            if ticker not in unique_ticers:
                tickers.append({
                    "ticker": ticker,
                    "name": name,
                    "sector": sector
                })
                unique_ticers.append(ticker)
        except Exception as e:
            logger.error(f"Error processing line: {line.strip()} - {e}")
with open("tickers.json", "w") as file:
    json.dump(tickers, file, indent=4)