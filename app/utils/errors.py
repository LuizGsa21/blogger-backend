from .tools import jsonify
from .constants import *


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


class PageNotFoundError(Error):
    status_code = HTTP_404_NOT_FOUND
    message = [{'detail': 'Page not found.', 'status': HTTP_404_NOT_FOUND}]


class LoginRequiredError(Error):
    status_code = HTTP_401_UNAUTHORIZED
    message = [{'detail': 'You must be logged in to access this endpoint.', 'status': HTTP_401_UNAUTHORIZED}]


class AdminRequiredError(Error):
    status_code = HTTP_403_FORBIDDEN
    message = [{'detail': 'You must be an admin to access this endpoint.', 'status': HTTP_403_FORBIDDEN}]

class CsrfTokenError(Error):
    status_code = HTTP_400_BAD_REQUEST
    message = [{'detail': 'Invalid CSRF token.', 'status': HTTP_400_BAD_REQUEST}]

class PermissionDeniedError(Error):
    status_code = HTTP_403_FORBIDDEN

    def __init__(self, action, resource):
        self.message = [
            {'detail': 'You do not have permission to %s this %s' % (action, resource), 'status': HTTP_403_FORBIDDEN}
        ]
