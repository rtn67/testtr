from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        # Import models
        from app.models import User, Robot, SubscriptionPlan
        
        # Create tables
        db.create_all()
        
        # Create default subscription plans if they don't exist
        if not SubscriptionPlan.query.first():
            default_plans = [
                SubscriptionPlan(
                    name='Free',
                    price_monthly=0,
                    price_yearly=0,
                    max_robots=1,
                    max_pairs=1,
                    features={'basic_dca': True}
                ),
                SubscriptionPlan(
                    name='Pro',
                    price_monthly=9.99,
                    price_yearly=99.99,
                    max_robots=5,
                    max_pairs=5,
                    features={'basic_dca': True, 'advanced_signals': True}
                ),
                SubscriptionPlan(
                    name='Enterprise',
                    price_monthly=29.99,
                    price_yearly=299.99,
                    max_robots=-1,
                    max_pairs=-1,
                    features={'basic_dca': True, 'advanced_signals': True, 'custom_signals': True}
                )
            ]
            for plan in default_plans:
                db.session.add(plan)
            db.session.commit()
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.trading import trading_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(trading_bp)
    
    return app