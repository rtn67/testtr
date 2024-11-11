import asyncio
import aiohttp
import os
from dotenv import load_dotenv
import logging
import platform
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Windows event loop policy
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test_proxy_connection():
    load_dotenv()
    
    # V2Ray proxy configuration
    proxy = 'http://127.0.0.1:10809'
    logger.info(f"Using proxy: {proxy}")
    
    # Test URLs (updated ticker format)
    urls = [
        'https://api.coinex.com/v1/market/list',
        'https://api.coinex.com/v1/market/ticker/BTC/USDT',  # Updated format
        'https://api.coinex.com/v1/market/ticker/all'
    ]
    
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        for url in urls:
            try:
                logger.info(f"\nTesting connection to: {url}")
                async with session.get(url, proxy=proxy) as response:
                    status = response.status
                    data = await response.json()
                    logger.info(f"Status: {status}")
                    logger.info(f"Response success: {data.get('code') == 0}")
                    if data.get('code') == 0:
                        logger.info("Sample data: " + json.dumps(data['data'])[:200])
                    
            except Exception as e:
                logger.error(f"Error connecting to {url}: {str(e)}")

def main():
    try:
        asyncio.run(test_proxy_connection())
    except Exception as e:
        logger.error(f"Main error: {str(e)}")

if __name__ == "__main__":
    main()