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


class lazy_property(object):
    def __init__(self, fget, class_property=True):
        self.fget = fget
        self.class_property = class_property
        self.func_name = fget.__name__

    def __get__(self, obj, cls):
        if self.class_property:
            value = self.fget(cls)
            setattr(cls, self.func_name, value)
            return value
        elif obj:
            value = self.fget(obj)
            setattr(obj, self.func_name, value)
            return value
        return None

