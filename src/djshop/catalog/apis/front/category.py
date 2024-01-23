from django.core.exceptions import (
    ObjectDoesNotExist, PermissionDenied, ValidationError as DjangoValidationError,
)
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.djshop.api.exception_handlers import hacksoft_proposed_exception_handler
from src.djshop.api.pagination import (
    CustomLimitOffsetPagination, get_paginated_response_context,
)
from src.djshop.catalog.selectors.category import (
    get_category_detail, get_category_list,
)
from src.djshop.catalog.serializers.front.category import (
    CategoryOutPutModelSerializer,
)


class CategoryListAPIView(APIView):

    """
    API view for retrieving a list of category.

    This view allows clients to retrieve a paginated
    list of category based on the provided filters.
    The view uses the `CategoryOutPutModelSerializer` to serialize
    the output representation of categories and
    the `CustomLimitOffsetPagination` class to paginate the results.

    Output Serializer:
        CategoryOutPutModelSerializer: Serializer for the output
        representation of categories.

    Pagination:
        CustomLimitOffsetPagination: Custom pagination class for a category list.

    Methods:
        get(self, request): Retrieve a paginated list of category based on
        the provided filters.

    """

    output_serializer = CategoryOutPutModelSerializer

    class Pagination(CustomLimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        responses=CategoryOutPutModelSerializer,
    )
    def get(self, request: 'Request') -> 'Response':

        """
        Retrieves a paginated list of categories based on the provided filters.

        This method allows clients to retrieve a paginated list of categories
        by sending a GET request to the category list endpoint with optional
        filter parameters. The results are then paginated using
        the `CustomLimitOffsetPagination` class and serialized using
        the `CategoryOutPutModelSerializer`.

        :param request: The request object.
        :return: Paginated response containing the list of categories.
        """

        try:
            category_list_queryset = get_category_list()

        except (
                DjangoValidationError, Http404, PermissionDenied, APIException
        ) as exc:

            exception_response = hacksoft_proposed_exception_handler(
                exc=exc, ctx={"request": request, "view": self}
            )

            assert exception_response is not None
            return Response(
                data=exception_response.data,
                status=exception_response.status_code,
            )

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.output_serializer,
            queryset=category_list_queryset,
            request=request,
            view=self,
        )


class CategoryDetailAPIView(APIView):

    """
    API view for retrieving a category detail.

    This view allows clients to retrieve the detailed representation of a category.
    The view uses the `CategoryDetailOutPutModelSerializer` to serialize the output
    representation of the category.

    Output Serializer:
        CategoryDetailOutPutModelSerializer: Serializer for the detailed
        representation of a category.

    :Methods:
        get (self, request, movie_slug): Retrieve the detail of a category
        based on the provided category slug.
    """

    category_output_serializer = CategoryOutPutModelSerializer

    @extend_schema(
        responses=CategoryOutPutModelSerializer,
    )
    def get(self, request: 'Request', category_slug: str) -> 'Response':
        """
        Retrieves the detail of a category based on the provided
        category slug.

        This method allows clients to retrieve the detailed
        representation of a category by sending a GET request
        to the category detail endpoint with the `category_slug` parameter.
        The method calls the `get_category_detail` function with
        the provided `category_slug` and current user to retrieve
        the detailed representation of the category.
        The result is then serialized using
        the `CategoryOutPutModelSerializer` and returned in the response.

        :param request: The request object.
        :param category_slug: (str): The slug of the category.
        :return: Response containing the detailed representation of the category.

        :raises DoesNotExist: If the category does not exist.
        """

        try:
            category_query = get_category_detail(category_slug=category_slug)

        except (
            DjangoValidationError, Http404, PermissionDenied, APIException,
            ObjectDoesNotExist
        ) as exc:

            exception_response = hacksoft_proposed_exception_handler(
                exc=exc, ctx={"request": request, "view": self}
            )

            assert exception_response is not None
            return Response(
                data=exception_response.data,
                status=exception_response.status_code,
            )

        output_serializer = self.category_output_serializer(
            instance=category_query
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)
