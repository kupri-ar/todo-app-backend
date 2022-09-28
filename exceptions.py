class BaseRequestException(Exception):
    def __init__(self, message=None, message_code=None, status_code=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if message_code is not None:
            self.message_code = message_code
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        if hasattr(self, 'message'):
            rv['message'] = self.message
        if hasattr(self, 'message_code'):
            rv['message_code'] = self.message_code
        return rv


class NotFoundException(BaseRequestException):
    status_code = 404
    message_code = 'NOT_FOUND'

    def __init__(self, message=None, message_code=None, status_code=None, payload=None):
        BaseRequestException.__init__(self, message, message_code, status_code, payload)


class MissingParam(BaseRequestException):
    status_code = 400
    message = 'Some request parameter is missing or the value is empty'
    message_code = 'MISSING_PARAM'

    def __init__(self, message=None, message_code=None, status_code=None, payload=None, param=None):
        if not message and param:
            message = "'{}' param is missing".format(param)
        BaseRequestException.__init__(self, message, message_code, status_code, payload)
