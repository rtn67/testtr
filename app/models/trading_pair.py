from app import db
from datetime import datetime

class TradingPair(db.Model):
    __tablename__ = 'trading_pairs'
    
    id = db.Column(db.Integer, primary_key=True)
    exchange_id = db.Column(db.Integer, db.ForeignKey('exchanges.id'))
    symbol = db.Column(db.String(20), nullable=False)
    base_currency = db.Column(db.String(10), nullable=False)
    quote_currency = db.Column(db.String(10), nullable=False)
    min_order_size = db.Column(db.Float)
    price_precision = db.Column(db.Integer)
    quantity_precision = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    exchange = db.relationship('Exchange', backref='trading_pairs')
    robots = db.relationship('Robot', backref='trading_pair')
    
    __table_args__ = (
        db.UniqueConstraint('exchange_id', 'symbol', name='unique_exchange_symbol'),
    )

    def __repr__(self):
        return f'<TradingPair {self.symbol} on {self.exchange.name}>'
