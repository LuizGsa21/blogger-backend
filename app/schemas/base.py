from marshmallow import (
    Schema as OSchema,
    fields,
    pre_dump,
    pre_load,
    SchemaOpts,
    ValidationError,
    post_dump
)
from .schema_helpers import FieldErrorFormatter as fe
from app.utils.errors import FieldError
from marshmallow.schema import VALIDATES

def fail(self, key, **kwargs):
    raise ValidationError(self.error_messages[key])


fields.Field.fail = fail


class Schema(OSchema):
    def __init__(self, *args, **kwargs):
        d_fields = self._declared_fields
        # customize require field error message based off the field attribute name
        for field_name, field in d_fields.iteritems():
            if field.required:
                field.error_messages['required'] = fe.field_require(field_name)
        super(Schema, self).__init__(*args, **kwargs)

    def handle_error(self, error, data):
        errors = []
        # if all http status match, then use it as the status code otherwise use 400 for general error.
        status_code = error.messages.itervalues().next()['status']
        for field, value in error.messages.iteritems():
            if status_code != 400 and value['status'] != status_code:
                status_code = 400
            errors.append(value)
        raise FieldError(errors, status_code=status_code)

    def validate_permission(self, data, original):
        if self.only:
            allowed_keys = self.only
        else:
            allowed_keys = self.opts.fields
        invalid_fields = []

        for fieldname in original.keys():
            if fieldname not in allowed_keys:
                invalid_fields.append(fe.field_permission_denied(fieldname))
        if invalid_fields:
            raise FieldError(invalid_fields, status_code=403)

    def _invoke_field_validators(self, data, many):
        for attr_name in self.__processors__[(VALIDATES, False)]:
            validator = getattr(self, attr_name)
            validator_kwargs = validator.__marshmallow_kwargs__[(VALIDATES, False)]
            field_name = validator_kwargs['field_name']

            try:
                field_obj = self.fields[field_name]
            except KeyError:
                if self.only and field_name not in self.only:
                    continue
                raise ValueError('"{0}" field does not exist.'.format(field_name))

            if many:
                for idx, item in enumerate(data):
                    try:
                        value = item[field_name]
                    except KeyError:
                        pass
                    else:
                        self._unmarshal.call_and_store(
                            getter_func=validator,
                            data=value,
                            field_name=field_name,
                            field_obj=field_obj,
                            index=(idx if self.opts.index_errors else None)
                        )
            else:
                try:
                    value = data[field_name]
                except KeyError:
                    pass
                else:
                    self._unmarshal.call_and_store(
                        getter_func=validator,
                        data=value,
                        field_name=field_name,
                        field_obj=field_obj
                    )

class Recursive(fields.Nested):
    def serialize(self, attr, obj, accessor=None):
        # pass same object to the nested schema
        return self._serialize(obj, attr, obj)


class ResourceOpts(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        self.type = getattr(meta, 'type', None)
        self.relationships = getattr(meta, 'relationships', {})


class ResourceSchema(Schema):
    id = fields.String(dump_only=True)
    OPTIONS_CLASS = ResourceOpts
    links = fields.Function(lambda obj: {'self': obj.url})

    def __init__(self, schema, param={}, *args, **kwargs):

        if not self.opts.type:
            raise ValueError('You must specify a `type` in Meta class')
        if not issubclass(schema, Schema):
            raise ValueError('Expected a schema as first argument')

        d_fields = self._declared_fields
        d_fields.update({'type': fields.String(self.opts.type)})
        d_fields.update({'attributes': Recursive(schema, **param)})
        super(ResourceSchema, self).__init__(*args, **kwargs)

    class Meta:
        fields = ('id', 'type', 'attributes', 'links', 'relationships')

    @pre_load(pass_many=True)
    def unwrap_data(self, data, many):
        if 'data' in data:
            data = data['data']
        return data
