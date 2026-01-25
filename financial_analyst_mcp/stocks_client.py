#!/usr/bin/env python

import os
import asyncio
import json
from mcp_openai import MCPClient, config
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


mcp_client_config = config.MCPClientConfig(
    mcpServers={
        "stocks": config.MCPServerConfig(
            command="uv",
            args=["run", "/Users/sdonapar/Documents/mcpdemo/financial_analyst_mcp/stocks_server.py"],
        )
        # add here other servers ...
    }
)

llm_client_config = config.LLMClientConfig(
    api_key=os.environ['OPENAI_API_KEY'],
    base_url="https://api.openai.com/v1",
)

llm_request_config = config.LLMRequestConfig(model="gpt-4o-mini")

client = MCPClient(
    mcp_client_config,
    llm_client_config,
    llm_request_config,
)

async def main():
    try:
        await client.connect_to_server("stocks")
        message_in=[
            {"role": "system", "content": "You are a helpful assistant that uses provided tools."},
            {"role": "user", "content": "Company details of Apple Inc"}
        ]
        message_out = await client.process_messages(message_in)
        result = message_out[4]['content']
        logger.info("Final Response:\n", result)
        with open("final_response.md", "w") as f:
            f.write(result) 
        # Access the final response content
    finally:
        # Properly close the client connection
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())