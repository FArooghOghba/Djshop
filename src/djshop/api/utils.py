from typing import Any, Dict, Optional, Type

from rest_framework import serializers


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
