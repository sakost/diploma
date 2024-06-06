from typing import Callable

from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger

from app.controllers.exeptions.exeptions import (
    AuthenticationFailed,
    BaseApiError,
    InvalidOperationError,
    InvalidTokenError,
    ServiceError,
    UserAlreadyExistsError,
    UserDoesNotExistError,
)


def create_exception_handler(
    status_code: int, initial_detail: str
) -> Callable[[Request, BaseApiError], JSONResponse]:
    detail = {"message": initial_detail}  # Using a dictionary to hold the detail

    async def exception_handler(_: Request, exc: BaseApiError) -> JSONResponse:
        if exc.message:
            detail["message"] = exc.message

        if exc.name:
            detail["message"] = f"{detail['message']} [{exc.name}]"

        logger.error(exc)
        return JSONResponse(
            status_code=status_code, content={"detail": detail["message"]}
        )

    return exception_handler


def add_all_handlers(app):
    app.add_exception_handler(
        exc_class_or_status_code=UserDoesNotExistError,
        handler=create_exception_handler(
            status.HTTP_404_NOT_FOUND, "User does not exist."
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=UserAlreadyExistsError,
        handler=create_exception_handler(
            status.HTTP_409_CONFLICT, "User already exist."
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=InvalidOperationError,
        handler=create_exception_handler(
            status.HTTP_400_BAD_REQUEST, "Can't perform the operation."
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=AuthenticationFailed,
        handler=create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            "Authentication failed due to invalid credentials.",
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=InvalidTokenError,
        handler=create_exception_handler(
            status.HTTP_401_UNAUTHORIZED, "Invalid token, please re-authenticate again."
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=ServiceError,
        handler=create_exception_handler(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "A service seems to be down, try again later.",
        ),
    )
