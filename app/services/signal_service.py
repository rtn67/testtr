import numpy as np
import pandas as pd
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class SignalService:
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """Calculate RSI indicator"""
        try:
            prices_array = np.array(prices)
            deltas = np.diff(prices_array)
            gain = deltas.copy()
            loss = deltas.copy()
            
            gain[gain < 0] = 0
            loss[loss > 0] = 0
            loss = abs(loss)
            
            avg_gain = np.mean(gain[:period])
            avg_loss = np.mean(loss[:period])
            
            if avg_loss == 0:
                return 100
                
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return round(rsi, 2)
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            return 50

    @staticmethod
    def calculate_macd(prices: List[float], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict:
        """Calculate MACD indicator"""
        try:
            prices_series = pd.Series(prices)
            
            # Calculate EMAs
            fast_ema = prices_series.ewm(span=fast_period, adjust=False).mean()
            slow_ema = prices_series.ewm(span=slow_period, adjust=False).mean()
            
            # Calculate MACD line
            macd_line = fast_ema - slow_ema
            
            # Calculate signal line
            signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
            
            # Calculate histogram
            histogram = macd_line - signal_line
            
            return {
                'macd': round(macd_line.iloc[-1], 8),
                'signal': round(signal_line.iloc[-1], 8),
                'histogram': round(histogram.iloc[-1], 8)
            }
            
        except Exception as e:
            logger.error(f"Error calculating MACD: {str(e)}")
            return {'macd': 0, 'signal': 0, 'histogram': 0}

    @staticmethod
    def calculate_moving_averages(prices: List[float], ma_type: str = "EMA", 
                                fast_period: int = 9, medium_period: int = 21, 
                                slow_period: int = 50) -> Dict:
        """Calculate moving averages"""
        try:
            prices_series = pd.Series(prices)
            
            if ma_type.upper() == "EMA":
                fast_ma = prices_series.ewm(span=fast_period, adjust=False).mean()
                medium_ma = prices_series.ewm(span=medium_period, adjust=False).mean()
                slow_ma = prices_series.ewm(span=slow_period, adjust=False).mean()
            else:  # SMA
                fast_ma = prices_series.rolling(window=fast_period).mean()
                medium_ma = prices_series.rolling(window=medium_period).mean()
                slow_ma = prices_series.rolling(window=slow_period).mean()
            
            return {
                'fast': round(fast_ma.iloc[-1], 8),
                'medium': round(medium_ma.iloc[-1], 8),
                'slow': round(slow_ma.iloc[-1], 8)
            }
            
        except Exception as e:
            logger.error(f"Error calculating moving averages: {str(e)}")
            return {'fast': 0, 'medium': 0, 'slow': 0}

    @staticmethod
    def analyze_signals(prices: List[float], robot_config: Dict) -> Dict:
        """Analyze all signals for a given robot configuration"""
        signals = {
            'rsi': None,
            'macd': None,
            'moving_averages': None,
            'entry_signal': False,
            'exit_signal': False
        }
        
        try:
            # RSI Analysis
            if robot_config.get('rsi', {}).get('enabled'):
                rsi_config = robot_config['rsi']
                rsi_value = SignalService.calculate_rsi(prices, rsi_config.get('period', 14))
                signals['rsi'] = {
                    'value': rsi_value,
                    'oversold': rsi_value <= rsi_config.get('oversold', 30),
                    'overbought': rsi_value >= rsi_config.get('overbought', 70)
                }
            
            # MACD Analysis
            if robot_config.get('macd', {}).get('enabled'):
                macd_config = robot_config['macd']
                macd_data = SignalService.calculate_macd(
                    prices,
                    macd_config.get('fast_period', 12),
                    macd_config.get('slow_period', 26),
                    macd_config.get('signal_period', 9)
                )
                signals['macd'] = {
                    'values': macd_data,
                    'bullish': macd_data['histogram'] > 0,
                    'bearish': macd_data['histogram'] < 0
                }
            
            # Moving Averages Analysis
            if robot_config.get('moving_averages', {}).get('enabled'):
                ma_config = robot_config['moving_averages']
                ma_data = SignalService.calculate_moving_averages(
                    prices,
                    ma_config.get('ma_type', 'EMA'),
                    ma_config.get('fast_ma', 9),
                    ma_config.get('medium_ma', 21),
                    ma_config.get('slow_ma', 50)
                )
                signals['moving_averages'] = {
                    'values': ma_data,
                    'bullish': ma_data['fast'] > ma_data['medium'] > ma_data['slow'],
                    'bearish': ma_data['fast'] < ma_data['medium'] < ma_data['slow']
                }
            
            # Combine Signals
            entry_conditions = []
            exit_conditions = []
            
            if signals['rsi']:
                entry_conditions.append(signals['rsi']['oversold'])
                exit_conditions.append(signals['rsi']['overbought'])
                
            if signals['macd']:
                entry_conditions.append(signals['macd']['bullish'])
                exit_conditions.append(signals['macd']['bearish'])
                
            if signals['moving