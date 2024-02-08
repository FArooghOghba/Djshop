from django.core.exceptions import (
    ObjectDoesNotExist, ValidationError as DjangoValidationError,
)
from django.db.utils import IntegrityError
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.djshop.api.exception_handlers import hacksoft_proposed_exception_handler
from src.djshop.api.pagination import (
    CustomLimitOffsetPagination, get_paginated_response_context,
)
from src.djshop.catalog.selectors.category import (
    get_category_node, get_category_tree,
)
from src.djshop.catalog.serializers.admin.category import (
    CategoryNodeInPutSerializer, CategoryNodeOutPutModelSerializer,
    CategoryTreeOutPutModelSerializer,
)
from src.djshop.catalog.services.category import (
    create_category_node, update_category_node,
)


class CategoryTreeAPIView(APIView):

    """
    API view for retrieving a list of category.

    This view allows clients to retrieve a paginated
    list of category based on the provided filters.
    The view uses the `CategoryTreeOutPutModelSerializer` to serialize
    the output representation of categories and
    the `CustomLimitOffsetPagination` class to paginate the results.

    Output Serializer:
        CategoryTreeOutPutModelSerializer: Serializer for the output
        representation of categories.

    Pagination:
        CustomLimitOffsetPagination: Custom pagination class for a category list.

    Methods:
        get(self, request): Retrieve a paginated list of category based on
        the provided filters.

    """

    output_serializer = CategoryTreeOutPutModelSerializer

    class Pagination(CustomLimitOffsetPagination):
        default_limit = 10

    @extend_schema(
        responses=CategoryTreeOutPutModelSerializer,
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
            category_list_queryset = get_category_tree()

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


class CategoryNodeAPIView(APIView):

    """
    API View for handling Category nodes.

    This view handles the creation of Category nodes and returns a serialized
    representation of the created Category node.

    Attributes:
        category_input_serializer (Serializer): The serializer for input data.
        category_output_serializer (Serializer): The serializer for output data.
    """

    category_input_serializer = CategoryNodeInPutSerializer
    category_output_serializer = CategoryNodeOutPutModelSerializer

    @extend_schema(
        responses=CategoryNodeOutPutModelSerializer,
    )
    def get(self, request: 'Request', category_slug: str) -> 'Response':

        """
        Retrieves the detail of a category based on the provided
        category slug.

        This method allows clients to retrieve the detailed
        representation of a category by sending a GET request
        to the category detail endpoint with the `category_slug` parameter.
        The method calls the `get_category_node` function with
        the provided `category_slug` and current user to retrieve
        the detailed representation of the category.
        The result is then serialized using
        the `CategoryNodeOutPutModelSerializer` and returned in the response.

        :param request: The request object.
        :param category_slug: (str): The slug of the category.
        :return: Response containing the detailed representation of the category.

        :raises DoesNotExist: If the category does not exist.
        """

        try:
            category_query = get_category_node(category_slug=category_slug)

        except (
                Http404, PermissionDenied, APIException, ObjectDoesNotExist
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

    @extend_schema(
        request=CategoryNodeInPutSerializer,
        responses=CategoryNodeOutPutModelSerializer
    )
    def put(self, request: 'Request', category_slug: str) -> 'Response':

        """
        Update the details of a category based on the provided
        category slug.

        This method allows clients to update the detailed representation
        of a category by sending a PUT request to the category detail
        endpoint with the `category_slug` parameter and providing the new
        category details in the request body.
        The method validates the input data using the `CategoryNodeInPutSerializer`
        and then updates the category node using the `update_category_node` function.
        The updated category node is serialized using
        the `CategoryNodeOutPutModelSerializer` and returned in the response.

        :param request: The request object.
        :param category_slug: The slug of the category.
        :return: Response containing the updated representation of the category.
        """

        input_serializer = self.category_input_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            # Extract the validated data from the serializer
            category_node_data = input_serializer.validated_data
            updated_category_node = update_category_node(
                category_slug=category_slug,
                category_node_data=category_node_data
            )

        except (
                DjangoValidationError, Http404, PermissionDenied, APIException,
                ObjectDoesNotExist, IntegrityError
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
            updated_category_node, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_202_ACCEPTED)

    @extend_schema(
        request=CategoryNodeInPutSerializer,
        responses=CategoryNodeOutPutModelSerializer
    )
    def patch(self, request: 'Request', category_slug: str) -> 'Response':

        """
        Partially update the details of a category based on the provided
        category slug.

        This method allows clients to partially update the detailed
        representation of a category by sending a PATCH request to
        the category detail endpoint with the `category_slug` parameter
        and providing the new category details in the request body.
        The method validates the input data using the `CategoryNodeInPutSerializer`
        with `partial=True`, indicating that partial updates are allowed.
        The category node is updated using the `update_category_node`
        function, and the updated category node is serialized using
        the `CategoryNodeOutPutModelSerializer` and returned in the response.

        :param request: The request object.
        :param category_slug: The slug of the category.
        :return: Response containing the updated representation of the category.
        """

        input_serializer = self.category_input_serializer(
            data=request.data, partial=True
        )
        input_serializer.is_valid(raise_exception=True)

        try:
            # Extract the validated data from the serializer
            category_node_data = input_serializer.validated_data

            updated_category_node = update_category_node(
                category_slug=category_slug,
                category_node_data=category_node_data
            )

        except (
                DjangoValidationError, Http404, PermissionDenied, APIException,
                ObjectDoesNotExist, IntegrityError
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
            updated_category_node, context={'request': request}
        )

        return Response(output_serializer.data, status=status.HTTP_202_ACCEPTED)


class CategoryNodeCreateAPIView(APIView):

    category_input_serializer = CategoryNodeInPutSerializer
    category_output_serializer = CategoryNodeOutPutModelSerializer

    @extend_schema(
        request=CategoryNodeInPutSerializer,
        responses=CategoryNodeOutPutModelSerializer
    )
    def post(self, request: 'Request') -> 'Response':

        """
        Handle POST requests.

        This method validates the input data using the category_input_serializer,
        creates a new Category node, and returns a serialized representation of the
        created Category node using the category_output_serializer.

        Args:
            request: The request object.

        Returns:
            Response: The response object.
        """

        input_serializer = self.category_input_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            # Extract the validated data from the serializer
            category_node_data = input_serializer.validated_data
            category_node = create_category_node(
                category_node_data=category_node_data
            )

        except (
            DjangoValidationError, Http404, PermissionDenied, APIException,
            ObjectDoesNotExist, IntegrityError
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
            category_node, context={'request': request}
        )
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
