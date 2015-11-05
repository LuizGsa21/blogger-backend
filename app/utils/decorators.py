from functools import wraps
from flask_login import current_user
from .tools import jsonify
from .constants import HTTP_403_FORBIDDEN
from errors import LoginRequiredError

def admin_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if not current_user.is_authenticated:
            raise LoginRequiredError()
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            response = jsonify(errors=[{'detail': 'You must be an admin to access this endpoint.'}])
            response.status_code = HTTP_403_FORBIDDEN
            return response

    return decorator

def login_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            raise LoginRequiredError()
    return decorator

