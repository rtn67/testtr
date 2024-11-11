import asyncio
import os
import ccxt.async_support as ccxt
from dotenv import load_dotenv
import logging
import platform

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_coinex_connection():
    exchange = None
    try:
        logger.info("Loading environment variables...")
        load_dotenv()
        
        api_key = os.getenv('COINEX_API_KEY')
        api_secret = os.getenv('COINEX_SECRET_KEY')
        
        logger.info(f"API Key present: {bool(api_key)}")
        logger.info(f"API Secret present: {bool(api_secret)}")
        
        logger.info("Initializing CoinEx connection...")
        exchange = ccxt.coinex({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'},
            'asyncio_loop': asyncio.get_event_loop()
        })
        
        # Test public endpoints
        logger.info("Testing public endpoints...")
        markets = await exchange.load_markets()
        logger.info(f"Successfully loaded {len(markets)} markets")
        
        # Get BTC/USDT ticker
        logger.info("Fetching BTC/USDT ticker...")
        ticker = await exchange.fetch_ticker('BTC/USDT')
        logger.info(f"BTC/USDT price: ${ticker['last']}")
        
        # Test authentication
        if api_key and api_secret:
            logger.info("Testing authenticated endpoints...")
            balance = await exchange.fetch_balance()
            logger.info("Successfully fetched balance")
            
        logger.info("All tests passed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error testing CoinEx connection: {str(e)}")
        return False
        
    finally:
        if exchange:
            await exchange.close()

def main():
    if platform.system() == 'Windows':
        # Set up proper event loop policy for Windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    loop = asyncio.get_event_loop()
    success = loop.run_until_complete(test_coinex_connection())
    
    if not success:
        logger.error("CoinEx connection test failed!")

if __name__ == "__main__":
    main()