from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from app.models.subscription import SubscriptionPlan

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    subscription_plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.id'))
    subscription_end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    robots = db.relationship('Robot', backref='user', lazy='dynamic')
    subscription = db.relationship('SubscriptionPlan', backref='users')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_robot_count(self):
        return self.robots.count()
    
    def can_create_robot(self):
        # Check subscription status
        if not self.subscription:
            # Free tier - 1 robot limit
            return self.get_robot_count() < 1
            
        if self.subscription_end_date and self.subscription_end_date < datetime.utcnow():
            # Expired subscription - free tier rules
            return self.get_robot_count() < 1
            
        # Check against subscription limit
        max_robots = self.subscription.max_robots
        if max_robots == -1:  # Unlimited
            return True
            
        return self.get_robot_count() < max_robots

    def __repr__(self):
        return f'<User {self.username}>'