from typing import Dict, List, Optional
import logging
from .base_exchange import BaseExchange
from .coinex_exchange import CoinExchange

logger = logging.getLogger(__name__)

class ExchangeFactory:
    """Factory class for creating exchange instances"""
    
    _exchanges: Dict[str, BaseExchange] = {}
    
    @classmethod
    async def get_exchange(cls, exchange_id: str) -> Optional[BaseExchange]:
        """Get or create an exchange instance"""
        try:
            if exchange_id not in cls._exchanges:
                exchange = cls._create_exchange(exchange_id)
                if exchange and await exchange.initialize():
                    cls._exchanges[exchange_id] = exchange
                else:
                    logger.error(f"Failed to initialize {exchange_id} exchange")
                    return None
            return cls._exchanges[exchange_id]
            
        except Exception as e:
            logger.error(f"Error getting exchange {exchange_id}: {str(e)}")
            return None
    
    @staticmethod
    def _create_exchange(exchange_id: str) -> Optional[BaseExchange]:
        """Create a new exchange instance"""
        exchanges = {
            'coinex': CoinExchange,
        }
        
        exchange_class = exchanges.get(exchange_id.lower())
        if exchange_class:
            return exchange_class()
        return None

    @classmethod
    def get_supported_exchanges(cls) -> List[str]:
        """Get list of supported exchanges"""
        return ['coinex']