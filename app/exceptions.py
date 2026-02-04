class APIException(Exception):
    status_code = 400
    message = "API Error"

    def __init__(self, message=None):
        if message:
            self.message = message


class NotFoundError(APIException):
    status_code = 404
    message = "Resource not found"


class UnauthorizedError(APIException):
    status_code = 401
    message = "Unauthorized"


class ForbiddenError(APIException):
    status_code = 403
    message = "Forbidden"


class ValidationError(APIException):
    status_code = 400
    message = "Invalid input"
