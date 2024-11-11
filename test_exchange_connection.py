import asyncio
import os
from dotenv import load_dotenv
from app.services.exchanges.exchange_factory import ExchangeFactory
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test database connection and fetch exchange configurations"""
    try:
        conn = psycopg2.connect(
            dbname="dca_trading_db",
            user="postgres",
            password="saman7721",
            host="localhost",
            port="5432"
        )
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Fetch active exchanges
        cur.execute("""
            SELECT id, name, api_config 
            FROM exchanges 
            WHERE is_active = true
        """)
        exchanges = cur.fetchall()
        
        # Fetch trading pairs
        cur.execute("""
            SELECT tp.*, e.name as exchange_name
            FROM trading_pairs tp
            JOIN exchanges e ON tp.exchange_id = e.id
            WHERE tp.is_active = true
        """)
        trading_pairs = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return exchanges, trading_pairs
        
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return None, None

async def test_exchange_connection(exchange_name: str):
    """Test connection to specific exchange"""
    try:
        exchange = await ExchangeFactory.get_exchange(exchange_name)
        if not exchange:
            logger.error(f"Failed to initialize {exchange_name} exchange")
            return

        logger.info(f"Testing {exchange_name.upper()} connection...")

        # Test market data
        logger.info("Fetching trading pairs...")
        pairs = await exchange.get_trading_pairs()
        logger.info(f"Found {len(pairs)} trading pairs")

        # Test specific pair (BTC/USDT)
        logger.info("Fetching BTC/USDT ticker...")
        ticker = await exchange.get_ticker('BTC/USDT')
        logger.info(f"BTC/USDT Price: ${ticker['last']}")

        # Test minimum order amount
        logger.info("Fetching minimum order amount...")
        min_amount = await exchange.get_min_order_amount('BTC/USDT')
        logger.info(f"Minimum BTC order amount: {min_amount}")

        # Test balance if API keys are set
        if os.getenv(f'{exchange_name.upper()}_API_KEY'):
            logger.info("Fetching USDT balance...")
            balance = await exchange.get_balance('USDT')
            logger.info(f"USDT Balance: ${balance}")

        logger.info(f"{exchange_name.upper()} connection test completed successfully")
        return True

    except Exception as e:
        logger.error(f"Exchange connection error: {str(e)}")
        return False

async def main():
    load_dotenv()
    
    # Test database connection
    logger.info("Testing database connection...")
    exchanges, trading_pairs = test_database_connection()
    
    if not exchanges:
        logger.error("Failed to fetch exchange configurations")
        return
    
    logger.info(f"Found {len(exchanges)} active exchanges")
    logger.info(f"Found {len(trading_pairs)} active trading pairs")
    
    # Test each active exchange
    for exchange in exchanges:
        await test_exchange_connection(exchange['name'])

if __name__ == "__main__":
    asyncio.run(main())