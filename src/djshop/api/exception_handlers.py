from typing import Any, Dict, Optional, Union

from django.core.exceptions import (
    ObjectDoesNotExist, PermissionDenied, ValidationError as DjangoValidationError,
)
from django.db.utils import IntegrityError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

from src.djshop.core.exceptions import ApplicationError


def drf_default_with_modifications_exception_handler(
    exc: Union[Exception, DjangoValidationError, Http404, PermissionDenied],
    ctx: Dict[str, str]
) -> Optional[Response]:

    """
    Custom exception handler that modifies the default
    Django Rest Framework exception handler.

    :param exc: The exception instance to be handled.
    :param ctx: A dictionary containing the request context.

    :return: A Response instance if the exception is recognized, otherwise None.
    """

    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    if hasattr(response, 'detail') and isinstance(response.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    return response


def hacksoft_proposed_exception_handler(
    exc: Union[
        DjangoValidationError, Http404, PermissionDenied, exceptions.APIException,
        ObjectDoesNotExist, IntegrityError
    ],
    ctx: Dict[str, Any]
) -> Optional[Response]:

    """
    Custom exception handler that modifies the default Django Rest Framework
    exception handler.

    This function handles various types of exceptions and returns a custom response
    for each one.
    If the exception is not recognized, it returns a generic error message.

    Args:
        exc (Union[DjangoValidationError, Http404, PermissionDenied, APIException,
            ObjectDoesNotExist, IntegrityError]): The exception instance to be
            handled.
        ctx (Dict[str, Any]): A dictionary containing the request context.

    Returns:
        Optional[Response]: A Response instance if the exception is recognized,
        otherwise None.
    """

    # Handle Django validation errors
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    # Handle 404 errors
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    # Handle permission denied errors
    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    # Handle an object does not exist errors
    if isinstance(exc, ObjectDoesNotExist):
        exc = exceptions.NotFound(f"Not Found - {exc}")

    # Handle integrity errors
    if isinstance(exc, IntegrityError):
        # Create a custom response for IntegrityError
        data = {
            "message": "A category with this title already exists.",
            "extra": {"error_message": str(exc)}
        }
        return Response(data, status=400)

    # Get the default DRF exception handler response
    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, ApplicationError):
            # Return a generic error message
            data = {
                "message": exc.message,
                "extra": exc.extra
            }
            return Response(data, status=500)

        else:
            # Return a generic error message
            data = {
                "message": "An unexpected error occurred.",
                "extra": {}
            }

            # HTTP status code for "Internal Server Error"
            return Response(data, status=500)

    # Customize the response data based on the type of exception
    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {
            "fields": response.data["detail"]
        }
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]

    return response
