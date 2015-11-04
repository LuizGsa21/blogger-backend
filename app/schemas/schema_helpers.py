from app.utils import constants as c


class FieldErrorFormatter(object):
    """Use FieldErrorFormatter to stay consistent with the error messages generate by the schemas"""

    @staticmethod
    def field_require(fieldname, status=c.HTTP_400_BAD_REQUEST):
        return {'detail': '"%s" field is required.' % fieldname, 'status': status}

    @staticmethod
    def field_conflict(fieldname, status=c.HTTP_409_CONFLICT):
        return {'detail': '"%s" field is required.' % fieldname, 'status': status}

    @staticmethod
    def field_permission_denied(fieldname, status=c.HTTP_403_FORBIDDEN):
        return {'detail': '"%s" you do not have permission to edit this field.' % fieldname, 'status': status}
