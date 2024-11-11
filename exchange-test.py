import asyncio
import os
from dotenv import load_dotenv
from app.services.exchanges.exchange_factory import ExchangeFactory

async def test_exchange(exchange_id: str):
    print(f"\nTesting {exchange_id.upper()} Exchange...")
    
    exchange = await ExchangeFactory.get_exchange(exchange_id)
    if not exchange:
        print(f"❌ Failed to initialize {exchange_id} exchange")
        return
    
    try:
        # Test getting trading pairs
        pairs = await exchange.get_trading_pairs()
        print("\n✅ Successfully fetched trading pairs")
        print(f"Found {len(pairs)} USDT trading pairs")
        print("\nSample pairs:")
        for pair in pairs[:5]:
            print(f"- {pair['symbol']}: Min Amount = {pair['min_amount']}")
        
        # Test getting ticker
        btc_ticker = await exchange.get_ticker('BTC/USDT')
        print("\n✅ Successfully fetched BTC/USDT ticker")
        print(f"Current BTC price: ${btc_ticker['last']}")
        
        # Test getting minimum order amount
        min_amount = await exchange.get_min_order_amount('BTC/USDT')
        print("\n✅ Successfully fetched minimum order amount")
        print(f"Minimum BTC order amount: {min_amount}")
        
        # Test balance (if API keys are set)
        if os.getenv(f'{exchange_id.upper()}_API_KEY'):
            balance = await exchange.get_balance('USDT')
            print("\n✅ Successfully fetched USDT balance")
            print(f"USDT Balance: ${balance}")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")

async def main():
    load_dotenv()
    
    # Get list of supported exchanges
    supported_exchanges = ExchangeFactory.get_supported_exchanges()
    print(f"Supported exchanges: {', '.join(supported_exchanges)}")
    
    # Test each supported exchange
    for exchange_id in supported_exchanges:
        await test_exchange(exchange_id)

if __name__ == "__main__":
    asyncio.run(main())
