from django.core.exceptions import (
    ObjectDoesNotExist, ValidationError as DjangoValidationError,
)
from django.db.utils import IntegrityError
from django.http import Http404
from drf_spectacular.utils import extend_schema
from requests import Request
from rest_framework import status
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from src.djshop.api.exception_handlers import hacksoft_proposed_exception_handler
from src.djshop.catalog.serializers.admin.category import (
    CategoryNodeInPutSerializer, CategoryTreeOutPutModelSerializer,
)
from src.djshop.catalog.services.category import create_category_node


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
    category_output_serializer = CategoryTreeOutPutModelSerializer

    @extend_schema(
        request=CategoryNodeInPutSerializer,
        responses=CategoryTreeOutPutModelSerializer
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
