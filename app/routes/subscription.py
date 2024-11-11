from flask import Blueprint

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/subscription')
def subscription_management():
    return 'Subscription management'