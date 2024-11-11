import aiohttp
import asyncio
import logging
import platform
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_coinex_endpoints():
    # List of CoinEx public endpoints to test
    endpoints = [
        'https://api.coinex.com/v1/market/list',
        'https://api.coinex.com/v1/market/ticker/all',
        'https://api.coinex.com/v1/market/ticker/BTC/USDT'
    ]
    
    async with aiohttp.ClientSession() as session:
        for endpoint in endpoints:
            try:
                logger.info(f"Testing endpoint: {endpoint}")
                start_time = datetime.now()
                
                async with session.get(endpoint) as response:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    status = response.status
                    data = await response.json()
                    
                    logger.info(f"Status: {status}")
                    logger.info(f"Response time: {elapsed:.2f} seconds")
                    logger.info(f"Response OK: {data.get('code') == 0}")
                    
            except Exception as e:
                logger.error(f"Error accessing {endpoint}: {str(e)}")

def main():
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_coinex_endpoints())

if __name__ == "__main__":
    main()
