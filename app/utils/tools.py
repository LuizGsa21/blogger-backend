from flask import jsonify as original_jsonify
from flask_login import current_user
from flask_wtf.csrf import generate_csrf


def jsonify(*args, **kwargs):
    if current_user.is_authenticated:
        if 'meta' in kwargs:
            kwargs['meta']['csrf_token'] = generate_csrf()
        else:
            kwargs['meta'] = {'csrf_token': generate_csrf()}

    return original_jsonify(*args, **kwargs)
