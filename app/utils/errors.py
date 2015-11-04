from flask import jsonify
from .constants import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED
)

class Error(Exception):
    def __init__(self, message=None, status_code=None):
        super(Error, self).__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def get_errors(self):
        return {'errors': self.message}


class FieldError(Error):
    status_code = HTTP_400_BAD_REQUEST


class LoginRequiredError(Error):
    status_code = HTTP_401_UNAUTHORIZED
    message = [{'detail': 'You must be logged in to access this endpoint.', 'status': HTTP_401_UNAUTHORIZED}]

class AdminRequiredError(Error):
    status_code = HTTP_403_FORBIDDEN
    message = [{'detail': 'You must be an admin to access this endpoint.', 'status': HTTP_403_FORBIDDEN}]
