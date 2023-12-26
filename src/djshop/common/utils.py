from typing import Any, Dict, List, Optional, Type, Union

from django.conf import settings
from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured

from rest_framework import serializers


def make_mock_object(**kwargs: Any) -> object:

    """
    Create a mock object with attributes defined by keyword arguments.

    :param: **kwargs: Arbitrary keyword arguments representing object attributes.
    :return: object: A dictionary representing the mock object with
            attributes defined by the provided keyword arguments.
    """

    return type("", (object, ), kwargs)


def get_object(
    *, model_or_queryset: Union[Type[Model], QuerySet[Model]],
    **kwargs: Optional[str]
) -> Optional[Model]:

    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None

    :param: model_or_queryset (Union[Model, QuerySet[Model]]): Either a Django Model
                            or a QuerySet of a specific Model.
    :param: **kwargs (Optional[str]): Arbitrary keyword arguments representing
                            lookup parameters.

    :return: Optional[Model]: The retrieved object if found, otherwise returns None.
    """

    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def create_serializer_class(
    *, name: str, fields: Dict[str, Type[serializers.Field[Any, Any, Any, Any]]]
) -> Type[Any]:

    """
    Create a dynamic serializer class based on provided fields.

    :param: name (str): The name for the new serializer class.
    :param: fields (Dict[str, Type[serializers.Field[Any, Any, Any, Any]]]):
                Dictionary representing serializer fields.

    :return: Type[Any]: A dynamically created serializer class.
    """

    return type(name, (serializers.Serializer, ), fields)


def inline_serializer(
    *, fields: Dict[str, Type[serializers.Field[Any, Any, Any, Any]]],
    data: Optional[Dict[str, Any]] = None, **kwargs: Optional[str]
) -> Any:

    """
    Create an inline serializer instance with specified fields.

    :param: fields (Dict[str, Type[serializers.Field[Any, Any, Any, Any]]]):
                    Dictionary representing serializer fields.
    :param: data (Optional[Dict[str, Any]]): Optional data to initialize
                    the serializer instance. Defaults to None.
    :param: **kwargs: Additional keyword arguments for serializer initialization.

    :return: Any: An instance of a dynamically created serializer
            class with specified fields.
    """

    serializer_class = create_serializer_class(name='', fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def assert_settings(
    *, required_settings: List[str], error_message_prefix: str = ""
) -> Union[Dict[str, Any], None]:

    """
    Check if each item from `required_settings` is present in Django settings.

    :param: required_settings (List[str]): List of required settings to be checked.
    :param: error_message_prefix (str, optional): Prefix for the error message.
                        Default to an empty string.

    :return: Dict[str, Any]: Dictionary containing the found settings and
                their values.

    :raise: ImproperlyConfigured: If any required setting is missing in
                Django settings.
    """

    not_present = []
    values = {}

    for required_setting in required_settings:
        if not hasattr(settings, required_setting):
            not_present.append(required_setting)
            continue

        values[required_setting] = getattr(settings, required_setting)

    if not_present:
        if not error_message_prefix:
            error_message_prefix = "Required settings not found."

        stringified_not_present = ", ".join(not_present)

        raise ImproperlyConfigured(
            f"{error_message_prefix} Could not find: {stringified_not_present}"
        )

    return values
