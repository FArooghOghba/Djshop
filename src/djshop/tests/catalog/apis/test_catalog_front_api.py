from typing import TYPE_CHECKING

import pytest
from django.urls import reverse
from rest_framework import status

from src.djshop.catalog.selectors.category import get_category_list
from src.djshop.catalog.serializers.front.category import (
    CategoryOutPutModelSerializer,
)


if TYPE_CHECKING:
    from rest_framework.test import APIClient, APIRequestFactory


pytestmark = pytest.mark.django_db


CATEGORY_LIST_URL = reverse('api:catalog:category-list')


def test_get_zero_category_should_return_empty_category_list(
    api_client: 'APIClient'
) -> None:

    """
    Test that requesting the category list with no categories returns an empty list.

    Args:
        api_client (APIClient): The Django REST framework API client.
    """

    response = api_client.get(path=CATEGORY_LIST_URL)
    assert response.status_code == status.HTTP_200_OK

    assert response.data['results'] == []


@pytest.mark.usefixtures('five_test_categories')
def test_get_five_categories_should_return_success(
    api_client: 'APIClient', api_request: 'APIRequestFactory'
) -> None:

    """
    Test that requesting the category list with five test categories
    returns the expected data.

    Args:
        api_client (APIClient): The Django REST framework API client.
        api_request (APIRequestFactory): The Django REST framework
                API request factory.
    """

    request = api_request.get(path=CATEGORY_LIST_URL)
    response = api_client.get(path=CATEGORY_LIST_URL, request=request)
    assert response.status_code == status.HTTP_200_OK

    # Get the queryset for all categories.
    test_categories_queryset = get_category_list()

    test_categories_output_serializer = CategoryOutPutModelSerializer(
        test_categories_queryset, many=True, context={'request': request}
    )
    assert response.data['results'] == test_categories_output_serializer.data
