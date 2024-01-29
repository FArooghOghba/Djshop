from typing import TYPE_CHECKING

import pytest
from django.db.models import QuerySet
from django.urls import reverse
from rest_framework import status

from src.djshop.catalog.models import Category


if TYPE_CHECKING:
    from rest_framework.test import APIClient, APIRequestFactory


pytestmark = pytest.mark.django_db


CATEGORY_ADMIN_DETAIL_URL = reverse('api:catalog:admin-category-node')


@pytest.mark.usefixtures('five_test_root_categories')
def test_create_admin_category_root_node_post_api_return_success(
        api_client: 'APIClient'
) -> None:

    """
    Test that an admin user can successfully create a category node through the API.

    This test ensures that an authorized admin user can create a valid category
    root node.
    The user's authentication is forced using the 'api_client.force_authenticate()'
    method, and the 'api_client.post()' method is used to post the category detail.

    :param api_client: An instance of the Django REST Framework's APIClient.

    :return: None
    """

    payload = {
        'title': 'Sixth Test Category',
        'description': 'This is the sixth test category.',
    }

    response = api_client.post(path=CATEGORY_ADMIN_DETAIL_URL, data=payload)
    assert response.status_code == status.HTTP_201_CREATED

    # Get the queryset for all categories.
    test_category_tree_queryset = Category.get_root_nodes()
    assert len(test_category_tree_queryset) == 6

    test_category_root_node = Category.get_last_root_node()
    test_category_root_node_title = test_category_root_node.title
    assert test_category_root_node_title == payload['title']

    get_category_root_node_response = response.data
    test_category_root_node_response_title = get_category_root_node_response['title']
    assert test_category_root_node_title == test_category_root_node_response_title


def test_create_admin_category_child_node_post_api_return_success(
        api_client: 'APIClient', api_request: 'APIRequestFactory',
        first_test_root_category: 'Category'
) -> None:

    """
    Test that an admin user can successfully create a category node through the API.

    This test ensures that an authorized admin user can create a valid category
    root node.
    The user's authentication is forced using the 'api_client.force_authenticate()'
    method, and the 'api_client.post()' method is used to post the category detail.

    :param api_client: An instance of the Django REST Framework's APIClient.

    :return: None
    """

    parent_slug = first_test_root_category.slug

    payload = {
        'title': 'First Test Child Category',
        'description': 'This is the first test child category.',
        'parent_node': parent_slug
    }

    response = api_client.post(path=CATEGORY_ADMIN_DETAIL_URL, data=payload)
    assert response.status_code == status.HTTP_201_CREATED

    # Get the queryset for the category tree.
    get_test_category_tree_queryset = Category.objects.filter(depth=1)
    assert len(get_test_category_tree_queryset) == 1

    get_test_category_node = get_test_category_tree_queryset[0]
    get_test_category_node_children: QuerySet['Category'] = (
        get_test_category_node.get_children()
    )
    assert len(get_test_category_node_children) == 1

    category_node_response = response.data
    category_node_response_title = category_node_response['title']

    get_test_category_child_node = get_test_category_node_children[0]
    category_child_node_expected_title = get_test_category_child_node.title
    assert category_node_response_title == category_child_node_expected_title


def test_create_admin_category_node_with_no_title_post_api_return_error(
        api_client: 'APIClient'
) -> None:

    """
    Test that the API returns an error when trying to create a category
    node with invalid data.

    This test ensures that the API correctly handles a situation where a
    client tries to create a category node with invalid data.
    The 'api_client.post()' method is used to post the category detail.

    :param api_client: An instance of the Django REST Framework's APIClient.

    :return: None
    """

    # This payload is missing the 'title' field, which is required
    # to create a category node
    payload = {
        'description': 'This is an invalid test category.',
    }

    response = api_client.post(path=CATEGORY_ADMIN_DETAIL_URL, data=payload)

    # Check that the API returned a 400 Bad Request status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Check that the error message in the response data is correct
    assert 'title' in response.data
    assert response.data['title'] == ['This field is required.']


def test_create_admin_category_node_with_nonexistent_parent_post_api_return_error(
        api_client: 'APIClient'
) -> None:

    """
    Test that the API returns an error when trying to create a category
    node with a non-existent parent.

    :param api_client: An instance of the Django REST Framework's APIClient.

    :return: None
    """

    # This payload includes a 'parent' field with a slug that doesn't exist
    # in the database
    payload = {
        'title': 'Test Category',
        'description': 'This is a test category.',
        'parent_node': 'nonexistent-parent-slug'
    }

    response = api_client.post(path=CATEGORY_ADMIN_DETAIL_URL, data=payload)

    # Check that the API returned a 400 Not Found status code
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Check that the error message in the response data is correct
    error_message = response.data['message']
    assert error_message == 'Not Found - Category matching query does not exist.'


def test_create_admin_category_node_with_duplicate_title_post_api_return_error(
        api_client: 'APIClient', first_test_root_category: 'Category'
) -> None:
    """
    Test that the API returns an error when trying to create a category
    node with a title that already exists.

    :param api_client: An instance of the Django REST Framework's APIClient.
    :param first_test_root_category: A category instance created for testing.

    :return: None
    """

    # This payload includes a 'title' field that already exists in the database
    payload = {
        'title': first_test_root_category.title,
        'description': 'This is a test category.',
    }

    response = api_client.post(path=CATEGORY_ADMIN_DETAIL_URL, data=payload)

    # Check that the API returned a 400 Bad Request status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Check that the error message in the response data is correct
    assert 'title' in response.data['extra']['error_message']
    assert response.data['message'] == 'A category with this title already exists.'
