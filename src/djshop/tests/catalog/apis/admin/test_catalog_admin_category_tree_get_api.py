from typing import TYPE_CHECKING, Dict

import pytest
from django.urls import reverse
from rest_framework import status

from src.djshop.catalog.selectors.admin.category import get_category_tree
from src.djshop.catalog.serializers.admin.category import (
    CategoryTreeOutPutModelSerializer,
)


if TYPE_CHECKING:
    from rest_framework.test import APIClient, APIRequestFactory

    from src.djshop.catalog.models import Category


pytestmark = pytest.mark.django_db


CATEGORY_ADMIN_TREE_URL = reverse('api:catalog:admin-category-tree')


@pytest.mark.usefixtures('five_test_root_categories')
def test_get_admin_category_tree_get_api_return_success(
    api_client: 'APIClient', api_request: 'APIRequestFactory'
) -> None:

    """
    Test that requesting the category list with five test categories
    returns the expected data.

    :param api_client (APIClient): The Django REST framework API client.
    :param api_request (APIRequestFactory): The Django REST framework
            API request factory.
    """

    request = api_request.get(path=CATEGORY_ADMIN_TREE_URL)
    response = api_client.get(path=CATEGORY_ADMIN_TREE_URL, request=request)
    assert response.status_code == status.HTTP_200_OK

    # Get the queryset for all categories.
    test_categories_queryset = get_category_tree()

    test_categories_output_serializer = CategoryTreeOutPutModelSerializer(
        test_categories_queryset, many=True, context={'request': request}
    )
    assert response.data['results'] == test_categories_output_serializer.data


def test_get_admin_category_tree_with_child_nodes_get_api_return_success(
    api_client: 'APIClient', api_request: 'APIRequestFactory',
    first_test_root_category: 'Category', second_test_root_category: 'Category',
    first_test_category_payload: Dict[str, str],
    second_test_category_payload: Dict[str, str]
) -> None:

    """
    Test that requesting the category list with five test categories
    returns the expected data.

    :param api_client (APIClient): The Django REST framework API client.
    :param api_request (APIRequestFactory): The Django REST framework
            API request factory.
    """

    first_test_root_category.add_child(**first_test_category_payload)
    second_test_root_category.add_child(**second_test_category_payload)

    request = api_request.get(path=CATEGORY_ADMIN_TREE_URL)
    response = api_client.get(path=CATEGORY_ADMIN_TREE_URL, request=request)
    assert response.status_code == status.HTTP_200_OK

    first_test_root_category_child = first_test_root_category.get_last_child()
    second_test_root_category_child = second_test_root_category.get_last_child()

    assert first_test_root_category_child is not None
    assert second_test_root_category_child is not None
    test_root_category_tree_children_title = [
        first_test_root_category_child.title, second_test_root_category_child.title
    ]

    get_category_tree_response = response.data['results']
    category_tree_children_response_title = [
        child['children'][0]['title'] for child in get_category_tree_response
    ]

    assert (category_tree_children_response_title ==
            test_root_category_tree_children_title)
