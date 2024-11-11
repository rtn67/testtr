import asyncio
import aiohttp
import logging
import platform
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_market_symbols():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.coinex.com/v1/market/ticker/all', proxy='http://127.0.0.1:10809') as response:
            data = await response.json()
            tickers = data.get('data', {}).get('ticker', {})
            
            logger.info("Available BTC markets:")
            btc_markets = [market for market in tickers.keys() if 'BTC' in market]
            logger.info(f"BTC markets: {btc_markets}")
            
            if 'BTCUSDT' in tickers:
                logger.info("Found BTCUSDT market!")
                logger.info(f"BTCUSDT ticker: {tickers['BTCUSDT']}")
            else:
                logger.info("BTCUSDT market not found!")
                logger.info(f"First 5 available markets: {list(tickers.keys())[:5]}")

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_market_symbols())