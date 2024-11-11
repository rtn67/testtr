import ccxt
import os
from datetime import datetime
import logging
from typing import Optional, Dict, List

class ExchangeService:
    def __init__(self, exchange_id='coinex'):
        self.exchange_id = exchange_id
        self.exchange = self._initialize_exchange()
        self.logger = logging.getLogger(__name__)

    def _initialize_exchange(self) -> ccxt.Exchange:
        """Initialize CoinEx exchange with API credentials"""
        exchange_class = getattr(ccxt, self.exchange_id)
        exchange = exchange_class({
            'apiKey': os.getenv('COINEX_API_KEY'),
            'secret': os.getenv('COINEX_SECRET_KEY'),
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',  # use spot trading
            }
        })
        return exchange

    async def get_balance(self, currency: str = 'USDT') -> float:
        """Get balance for a specific currency"""
        try:
            balance = await self.exchange.fetch_balance()
            return float(balance[currency]['free']) if currency in balance else 0.0
        except Exception as e:
            self.logger.error(f"Error fetching balance: {str(e)}")
            raise

    async def get_ticker(self, symbol: str) -> Dict:
        """Get current ticker information for a trading pair"""
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            return {
                'last': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'volume': ticker['baseVolume'],
                'timestamp': ticker['timestamp']
            }
        except Exception as e:
            self.logger.error(f"Error fetching ticker for {symbol}: {str(e)}")
            raise

    async def create_market_buy_order(self, symbol: str, amount: float) -> Dict:
        """Create a market buy order"""
        try:
            order = await self.exchange.create_market_buy_order(symbol, amount)
            return {
                'id': order['id'],
                'symbol': order['symbol'],
                'type': order['type'],
                'side': order['side'],
                'amount': order['amount'],
                'price': order['price'],
                'cost': order['cost'],
                'status': order['status']
            }
        except Exception as e:
            self.logger.error(f"Error creating market buy order: {str(e)}")
            raise

    async def get_min_order_amount(self, symbol: str) -> float:
        """Get minimum order amount for a trading pair"""
        try:
            markets = await self.exchange.fetch_markets()
            market = next((m for m in markets if m['symbol'] == symbol), None)
            if market:
                return float(market['limits']['amount']['min'])
            raise ValueError(f"Symbol {symbol} not found")
        except Exception as e:
            self.logger.error(f"Error fetching minimum order amount: {str(e)}")
            raise

    async def get_trading_pairs(self) -> List[Dict]:
        """Get available trading pairs from CoinEx"""
        try:
            markets = await self.exchange.fetch_markets()
            return [
                {
                    'symbol': market['symbol'],
                    'base': market['base'],
                    'quote': market['quote'],
                    'min_amount': float(market['limits']['amount']['min']),
                    'min_cost': float(market['limits']['cost']['min']) if 'min' in market['limits']['cost'] else 0,
                    'price_precision': market['precision']['price'],
                    'amount_precision': market['precision']['amount']
                }
                for market in markets
                if market['active'] and 'USDT' in market['symbol']  # Filter for USDT pairs
            ]
        except Exception as e:
            self.logger.error(f"Error fetching trading pairs: {str(e)}")
            raise

    async def get_order_status(self, order_id: str, symbol: str) -> Dict:
        """Get status of a specific order"""
        try:
            order = await self.exchange.fetch_order(order_id, symbol)
            return {
                'id': order['id'],
                'status': order['status'],
                'filled': order['filled'],
                'remaining': order['remaining'],
                'cost': order['cost'],
                'average': order['average']
            }
        except Exception as e:
            self.logger.error(f"Error fetching order status: {str(e)}")
            raise