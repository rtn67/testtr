import os
from app import create_app, db
from app.models.user import User
from app.models.robot import Robot, TradingPair
from app.models.subscription import SubscriptionPlan, UserSubscription
from datetime import datetime, timedelta

def test_database_setup():
    """Test database connections and model creation"""
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        try:
            # Create test subscription plan
            free_plan = SubscriptionPlan(
                name='Free',
                price_monthly=0,
                price_yearly=0,
                max_robots=1,
                max_pairs=1,
                features={"basic_dca": True}
            )
            db.session.add(free_plan)
            
            # Create test trading pair
            btc_usdt = TradingPair(
                exchange='binance',
                symbol='BTC/USDT',
                base_currency='BTC',
                quote_currency='USDT',
                min_order_size=0.0001,
                is_active=True
            )
            db.session.add(btc_usdt)
            
            # Create test user
            test_user = User(
                email='test@example.com',
                username='test_user',
                subscription_tier='free'
            )
            test_user.set_password('password123')
            db.session.add(test_user)
            
            # Commit the changes
            db.session.commit()
            
            # Create test robot
            test_robot = Robot(
                name='Test BTC DCA Bot',
                user_id=test_user.id,
                trading_pair_id=btc_usdt.id,
                base_order_amount=10.0,  # 10 USDT per order
                interval_hours=24,
                status='inactive'
            )
            db.session.add(test_robot)
            
            # Create test subscription
            test_subscription = UserSubscription(
                user_id=test_user.id,
                plan_id=free_plan.id,
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=30),
                payment_status='active'
            )
            db.session.add(test_subscription)
            
            # Commit all changes
            db.session.commit()
            
            print("✅ Database setup successful!")
            print("✅ Test data created successfully!")
            
            # Verify data
            print("\nVerifying created data:")
            print(f"User: {User.query.first()}")
            print(f"Trading Pair: {TradingPair.query.first()}")
            print(f"Robot: {Robot.query.first()}")
            print(f"Subscription Plan: {SubscriptionPlan.query.first()}")
            print(f"User Subscription: {UserSubscription.query.first()}")
            
        except Exception as e:
            print(f"❌ Error during setup: {str(e)}")
            db.session.rollback()
        
if __name__ == "__main__":
    test_database_setup()
