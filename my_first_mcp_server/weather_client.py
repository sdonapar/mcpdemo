#!/usr/bin/env python

import sys
from fastmcp import Client
import asyncio
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO, # Set the minimum logging level to output (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

async def main():
    # The client infers the transport (e.g., Stdio) from the input string.
    #async with Client("weather.py") as client:
    async with Client("http://localhost:8000/sse") as client:
        # List available tools on the server
        tools = await client.list_tools()
        logger.info("Available tools:", tools)

        # Call a specific tool ("add") with arguments
        result = await client.call_tool("get_alerts", {"state": "TX"})
        logger.info("Result:", result.content[0].text) # Access the result data

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())