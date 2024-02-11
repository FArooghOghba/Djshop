from typing import TYPE_CHECKING

import pytest
from django.db.models import QuerySet
from django.urls import reverse
from rest_framework import status

from src.djshop.catalog.selectors.front.category import get_category_tree
from src.djshop.catalog.serializers.front.category import (
    CategoryOutPutModelSerializer,
)


if TYPE_CHECKING:
    from rest_framework.test import APIClient, APIRequestFactory

    from src.djshop.catalog.models import Category


pytestmark = pytest.mark.django_db


CATEGORY_FRONT_LIST_URL = reverse('api:catalog:front-category-list')


def test_get_zero_front_category_tree_get_api_return_empty(
    api_client: 'APIClient'
) -> None:

    """
    Test that requesting the category list with no categories returns an empty list.

    :param api_client (APIClient): The Django REST framework API client.
    """

    response = api_client.get(path=CATEGORY_FRONT_LIST_URL)
    assert response.status_code == status.HTTP_200_OK

    assert response.data['results'] == []


@pytest.mark.usefixtures('five_test_root_categories')
def test_get_front_category_tree_get_api_return_success(
    api_client: 'APIClient', api_request: 'APIRequestFactory'
) -> None:

    """
    Test that requesting the category list with five test categories
    returns the expected data.

    :param api_client (APIClient): The Django REST framework API client.
    :param api_request (APIRequestFactory): The Django REST framework
            API request factory.
    """

    request = api_request.get(path=CATEGORY_FRONT_LIST_URL)
    response = api_client.get(path=CATEGORY_FRONT_LIST_URL, request=request)
    assert response.status_code == status.HTTP_200_OK

    # Get the queryset for all categories.
    test_categories_queryset = get_category_tree()

    test_categories_output_serializer = CategoryOutPutModelSerializer(
        test_categories_queryset, many=True, context={'request': request}
    )
    assert response.data['results'] == test_categories_output_serializer.data

    test_categories = response.data['results']
    for test_category in test_categories:
        assert test_category['is_public'] is True


def test_get_front_category_public_tree_get_api_return_error(
    api_client: 'APIClient', api_request: 'APIRequestFactory',
    five_test_root_categories: QuerySet['Category']
) -> None:

    """
    Test that requesting the category list with five test categories
    returns the expected data.

    :param api_client (APIClient): The Django REST framework API client.
    :param api_request (APIRequestFactory): The Django REST framework
            API request factory.
    """

    first_test_category = five_test_root_categories[0]
    first_test_category.is_public = False
    first_test_category.save()

    second_test_category = five_test_root_categories[1]
    second_test_category.is_public = False
    second_test_category.save()

    request = api_request.get(path=CATEGORY_FRONT_LIST_URL)
    response = api_client.get(path=CATEGORY_FRONT_LIST_URL, request=request)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 3

    # Get the queryset for all categories.
    test_categories_queryset = get_category_tree()

    test_categories_output_serializer = CategoryOutPutModelSerializer(
        test_categories_queryset, many=True, context={'request': request}
    )
    assert response.data['results'] == test_categories_output_serializer.data

    test_categories = response.data['results']
    for test_category in test_categories:
        assert test_category['is_public'] is True
