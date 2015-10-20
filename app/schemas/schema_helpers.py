

def require(fieldname, status=400):
    return {fieldname: '%s field is required.' % fieldname, 'status': 400}