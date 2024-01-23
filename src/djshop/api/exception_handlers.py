from typing import Any, Dict, Optional, Union

from django.core.exceptions import (
    ObjectDoesNotExist, PermissionDenied, ValidationError as DjangoValidationError,
)
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
        ObjectDoesNotExist
    ],
    ctx: Dict[str, Any]
) -> Optional[Response]:

    """
    Custom exception handler that modifies the default Django Rest Framework
    exception handler.

    :param: exc (Union[
                DjangoValidationError, Http404, PermissionDenied,
                exceptions.APIException, ObjectDoesNotExist
                ]
        ): The exception instance to be handled.
    :param: ctx (Any): A dictionary containing the request context.

    :return: Optional[Response]: A Response instance if the exception is
                recognized, otherwise None.
    """

    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, ObjectDoesNotExist):
        exc = exceptions.NotFound(f"Not Found - {exc}")

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, ApplicationError):
            data = {
                "message": exc.message,
                "extra": exc.extra
            }
            return Response(data, status=400)

        else:
            # Return a generic error message
            data = {
                "message": "An unexpected error occurred.",
                "extra": {}
            }

            # HTTP status code for "Internal Server Error"
            return Response(data, status=500)

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
