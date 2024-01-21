from collections import OrderedDict
from typing import Any, List, Type, Union

from django.db.models import QuerySet
from rest_framework.pagination import BasePagination, LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView


def get_paginated_response(
    *, pagination_class: Type[BasePagination],
    serializer_class: Type[BaseSerializer[Any]],
    queryset: QuerySet[Any], request: Request, view: APIView
) -> Response:

    """
    Generate paginated response for a given queryset using specified
    pagination and serializer classes.

    :param: pagination_class (Type[BasePagination]): Pagination class instance
                    to handle pagination logic.
    :param: serializer_class (Type[BaseSerializer[Any]]): Serializer class used
                    to serialize the queryset.
    :param: queryset (QuerySet[Any]): QuerySet to be paginated and serialized.
    :param: request (Request): HTTP request object.
    :param: view (APIView): APIView instance.

    :return: Response: Paginated response containing serialized data.
    """

    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)


def get_paginated_response_context(
    *, pagination_class: Type[BasePagination],
    serializer_class: Type[BaseSerializer[Any]],
    queryset: QuerySet[Any], request: Request, view: APIView
) -> Response:

    """
    Generate paginated response with context for a given queryset using specified
    pagination and serializer classes.

    :param: pagination_class (Type[BasePagination]): Pagination class type
                            to handle pagination logic.
    :param: serializer_class (Type[BaseSerializer[Any]]): Serializer class type used
                            to serialize the queryset.
    :param: queryset (QuerySet[Any]): QuerySet to be paginated and serialized.
    :param: request (Request): HTTP request object.
    :param: view (APIView): APIView instance.

    :return: Response: Paginated response containing serialized data.
    """

    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True, context={'request': request})

    return Response(data=serializer.data)


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_paginated_data(
            self, data: List[object]
    ) -> OrderedDict[str, Union[int, str, List[object], None]]:

        """
        Generate paginated data containing limit, offset, count, next, previous,
        and results.

        :param: data (List[Any]): Data to be paginated.

        :return: OrderedDict: Paginated data containing metadata and results.
        """

        return OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

    def get_paginated_response(self, data: List[object]) -> Response:

        """
        Generate paginated response including limit, offset, count, next,
        previous, and results.

        We redefine this method to include `limit` and `offset` in the response.
        This information is used by the frontend for pagination.

        :param: data (List[Any]): Data to be included in the response.

        :return: Response: Paginated response containing metadata and results.
        """

        return Response(OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
