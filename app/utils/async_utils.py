from functools import wraps
from asgiref.sync import async_to_sync

def async_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return async_to_sync(f)(*args, **kwargs)
    return decorated_function