from flask import Blueprint

robot_bp = Blueprint('robot', __name__)

@robot_bp.route('/robots')
def list_robots():
    return 'Robots list'