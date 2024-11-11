from app import db
from datetime import datetime

class Robot(db.Model):
    __tablename__ = 'robots'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exchange_id = db.Column(db.Integer, db.ForeignKey('exchanges.id'))
    trading_pair_id = db.Column(db.Integer, db.ForeignKey('trading_pairs.id'))
    status = db.Column(db.String(20), default='inactive')  # inactive, active, error
    
    # Trading Configuration
    initial_investment = db.Column(db.Float, nullable=False)
    entry_type = db.Column(db.String(20), default='signal')  # signal, manual
    
    # Signal and DCA Configuration
    signal_config = db.Column(db.JSON)
    dca_config = db.Column(db.JSON)
    
    # Position Management
    entry_price = db.Column(db.Float)
    average_entry_price = db.Column(db.Float)
    current_position = db.Column(db.Float)
    peak_price = db.Column(db.Float)
    total_invested = db.Column(db.Float, default=0.0)
    unrealized_pnl = db.Column(db.Float)
    
    # Order Management
    total_orders = db.Column(db.Integer, default=0)
    dca_orders_placed = db.Column(db.Integer, default=0)
    last_order_time = db.Column(db.DateTime)
    last_signal_time = db.Column(db.DateTime)
    
    # Exit Configuration
    take_profit = db.Column(db.Float)
    stop_loss = db.Column(db.Float)
    trailing_stop = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships are already defined via backref in User and TradingPair models
    
    def __repr__(self):
        return f'<Robot {self.name}>'