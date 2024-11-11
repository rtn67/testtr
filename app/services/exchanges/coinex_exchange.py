import aiohttp
import os
from typing import Dict, List, Optional
from .base_exchange import BaseExchange
import logging
import asyncio
import platform
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class CoinExchange(BaseExchange):
    """CoinEx exchange implementation"""
    
    def __init__(self):
        super().__init__()
        self.base_url = 'https://api.coinex.com/v1'
        self.proxy = 'http://127.0.0.1:10809'
        self.markets = {}
        self.tickers = {}
        
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def _make_request(self, endpoint: str, method: str = 'GET', params: Dict = None) -> Dict:
        url = f"{self.base_url}/{endpoint}"
        logger.info(f"Making {method} request to: {url}")
        
        try:
            connector = aiohttp.TCPConnector(ssl=False)
            timeout = aiohttp.ClientTimeout(total=30)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                kwargs = {'proxy': self.proxy}
                if params:
                    kwargs['params'] = params
                    
                async with session.request(method, url, **kwargs) as response:
                    text = await response.text()
                    logger.info(f"Response status: {response.status}")
                    logger.info(f"Raw response: {text[:200]}...")
                    
                    if response.status != 200:
                        logger.error(f"Error response: {text}")
                        raise Exception(f"HTTP {response.status}: {text}")
                    
                    data = json.loads(text)
                    if data.get('code') != 0:
                        raise Exception(data.get('message', 'Unknown error'))
                    
                    return data.get('data')
                    
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    def _convert_to_market_id(self, symbol: str) -> str:
        """Convert symbol format (e.g., 'BTC/USDT' to 'BTCUSDT')"""
        return symbol.replace('/', '')

    def _convert_to_symbol(self, market_id: str) -> str:
        """Convert market ID format (e.g., 'BTCUSDT' to 'BTC/USDT')"""
        if market_id.endswith('USDT'):
            base = market_id[:-4]
            return f"{base}/USDT"
        return market_id

    async def initialize(self) -> bool:
        try:
            logger.info("Initializing CoinEx exchange")
            
            # Get market info
            self.markets = await self._make_request('market/info')
            logger.info(f"Loaded {len(self.markets)} markets")
            
            # Get initial tickers
            data = await self._make_request('market/ticker/all')
            self.tickers = data.get('ticker', {})
            
            # Verify we can access BTCUSDT market
            btc_ticker = self.tickers.get('BTCUSDT')
            if not btc_ticker:
                raise Exception("Unable to access BTCUSDT market")
                
            logger.info(f"Successfully initialized CoinEx exchange. BTC price: ${btc_ticker['last']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize CoinEx: {str(e)}")
            return False

    async def get_balance(self, currency: str = 'USDT') -> float:
        return 1000.0  # Mock balance

    async def create_market_buy_order(self, symbol: str, amount: float) -> Dict:
        return {
            'id': 'mock-order-id',
            'symbol': symbol,
            'type': 'market',
            'side': 'buy',
            'amount': amount,
            'status': 'closed'
        }

    async def get_min_order_amount(self, symbol: str) -> float:
        market_id = self._convert_to_market_id(symbol)
        market_info = self.markets.get(market_id, {})
        return float(market_info.get('min_amount', 0.0001))

    async def get_order_status(self, order_id: str, symbol: str) -> Dict:
        return {
            'id': order_id,
            'symbol': symbol,
            'status': 'closed',
            'filled': 1.0,
            'remaining': 0.0,
            'average': 0.0
        }

    async def get_trading_pairs(self) -> List[Dict]:
        try:
            logger.info("Fetching trading pairs")
            
            # Update tickers
            data = await self._make_request('market/ticker/all')
            self.tickers = data.get('ticker', {})
            
            pairs = []
            for market_id, ticker in self.tickers.items():
                if market_id.endswith('USDT'):
                    market_info = self.markets.get(market_id, {})
                    symbol = self._convert_to_symbol(market_id)
                    
                    pairs.append({
                        'symbol': symbol,
                        'base': symbol.split('/')[0],
                        'quote': 'USDT',
                        'last_price': float(ticker.get('last', 0)),
                        'volume_24h': float(ticker.get('vol', 0)),
                        'change_24h': float(ticker.get('change', 0)) if 'change' in ticker else 0,
                        'high_24h': float(ticker.get('high', 0)),
                        'low_24h': float(ticker.get('low', 0)),
                        'min_amount': float(market_info.get('min_amount', 0.0001)),
                        'price_decimal': int(market_info.get('pricing_decimal', 8))
                    })
            
            logger.info(f"Successfully fetched {len(pairs)} trading pairs")
            return pairs
            
        except Exception as e:
            logger.error(f"Error fetching trading pairs: {str(e)}")
            raise

    async def get_ticker(self, symbol: str) -> Dict:
        try:
            logger.info(f"Fetching ticker for {symbol}")
            
            # Update tickers
            data = await self._make_request('market/ticker/all')
            self.tickers = data.get('ticker', {})
            
            market_id = self._convert_to_market_id(symbol)
            ticker = self.tickers.get(market_id)
            
            if not ticker:
                logger.error(f"No ticker found for {market_id}")
                available_markets = list(self.tickers.keys())[:5]
                logger.info(f"Available markets (first 5): {available_markets}")
                raise Exception(f"Ticker not found for {market_id}")
            
            return {
                'symbol': symbol,
                'last': float(ticker.get('last', 0)),
                'bid': float(ticker.get('buy', 0)),
                'ask': float(ticker.get('sell', 0)),
                'volume': float(ticker.get('vol', 0)),
                'high': float(ticker.get('high', 0)),
                'low': float(ticker.get('low', 0)),
                'change': float(ticker.get('change', 0)) if 'change' in ticker else 0
            }
            
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol}: {str(e)}")
            raise