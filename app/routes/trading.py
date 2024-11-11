from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required
from app.utils.async_utils import async_route
from app.services.exchanges import ExchangeFactory

from app.utils.trading import calculate_dca_orders
import logging

trading_bp = Blueprint('trading', __name__)
logger = logging.getLogger(__name__)

@trading_bp.route('/api/trading/pairs/by-quote/<quote_currency>')
@login_required
@async_route
async def get_pairs_by_quote(quote_currency):

    """Get trading pairs filtered by quote currency"""
    try:
        exchange_name = request.args.get('exchange', 'coinex')
        logger.info(f"Fetching {quote_currency} pairs for {exchange_name}")
        
        exchange = await ExchangeFactory.get_exchange(exchange_name)
        if not exchange:
            return jsonify({
                'status': 'error',
                'message': 'Exchange not available'
            }), 400
        
        # Get all pairs and filter by quote currency
        all_pairs = await exchange.get_trading_pairs()
        filtered_pairs = [
            pair for pair in all_pairs 
            if pair['quote'] == quote_currency
        ]
        
        # Sort by volume
        sorted_pairs = sorted(
            filtered_pairs, 
            key=lambda x: float(x.get('volume_24h', 0)), 
            reverse=True
        )
        
        return jsonify({
            'success': True,
            'count': len(sorted_pairs),
            'pairs': sorted_pairs
        })
        
    except Exception as e:
        logger.error(f"Error fetching trading pairs: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
 # Add this to your existing trading.py routes

@trading_bp.route('/trading/bot/configure')
@login_required
def configure_bot():
    """Bot configuration page"""
    return render_template('trading/bot/configure.html')

@trading_bp.route('/api/trading/bot/calculate', methods=['POST'])
@login_required
def calculate_orders():
    """Calculate DCA orders based on configuration"""
    try:
        data = request.json
        calculations = calculate_dca_orders(data)
        return jsonify({
            'status': 'success',
            'data': calculations
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400       