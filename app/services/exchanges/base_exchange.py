from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import logging

class BaseExchange(ABC):
    """Base class for all exchange implementations"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize exchange connection"""
        pass

    @abstractmethod
    async def get_balance(self, currency: str) -> float:
        """Get balance for specific currency"""
        pass

    @abstractmethod
    async def get_ticker(self, symbol: str) -> Dict:
        """Get current price information"""
        pass

    @abstractmethod
    async def create_market_buy_order(self, symbol: str, amount: float) -> Dict:
        """Create market buy order"""
        pass

    @abstractmethod
    async def get_min_order_amount(self, symbol: str) -> float:
        """Get minimum order amount for symbol"""
        pass

    @abstractmethod
    async def get_trading_pairs(self) -> List[Dict]:
        """Get available trading pairs"""
        pass

    @abstractmethod
    async def get_order_status(self, order_id: str, symbol: str) -> Dict:
        """Get status of specific order"""
        pass