class BaseApiError(Exception):
    def __init__(self, message: str = "Service not available", name: str = "Default"):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class ServiceError(BaseApiError):
    """failures in external services or APIs, like a database or a third-party service"""

    pass


class UserDoesNotExistError(BaseApiError):
    """database returns nothing"""

    pass


class UserAlreadyExistsError(BaseApiError):
    """conflict detected, like trying to create a resource that already exists"""

    pass


class InvalidOperationError(BaseApiError):
    """invalid operations like trying to delete a non-existing entity, etc."""

    pass


class AuthenticationFailed(BaseApiError):
    """invalid authentication credentials"""

    pass


class InvalidTokenError(BaseApiError):
    """invalid token"""

    pass


# etc
