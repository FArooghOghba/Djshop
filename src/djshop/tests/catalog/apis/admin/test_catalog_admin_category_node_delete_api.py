from typing import TYPE_CHECKING

import pytest
from django.db.models import QuerySet
from django.urls import reverse
from rest_framework import status

from src.djshop.catalog.models import Category


if TYPE_CHECKING:
    from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


def category_admin_node_url(category_slug: str) -> str:

    """
    Generate the URL for the category admin node get API endpoint based on
    the category slug.

    This function takes a category slug as input and generates the URL for the
    category admin node get API endpoint by using the `reverse` function provided
    by Django's URL resolver. The category slug is included as a parameter in
    the URL.

    :param category_slug: The slug of the category.
    :return: The URL for the category admin 'node get API' endpoint.
    """

    return reverse(
        viewname='api:catalog:admin-category-node', args=[category_slug]
    )


def test_destroy_admin_category_node_delete_api_return_success(
    api_client: 'APIClient', five_test_root_categories: QuerySet['Category']
) -> None:

    """
    Test that a admin user can successfully delete category node for through the API.

    This test ensures that an authorized admin user can delete a category node.
    The admin user using the 'api_client.delete()' method is used to delete
    the category.

    :param api_client: An instance of the Django REST Framework's APIClient.
    :param five_test_root_categories: A fixture providing the category queryset.
    :return: None
    """

    test_category = five_test_root_categories[0]

    # Delete the category node with category slug.
    url = category_admin_node_url(
        category_slug=test_category.slug,
    )
    delete_category_response = api_client.delete(
        path=url,
    )
    assert delete_category_response.status_code == status.HTTP_204_NO_CONTENT

    # Assertion: Check that the category is successfully deleted.
    category_root_nodes = Category.get_root_nodes()
    category_root_nodes_counts = len(category_root_nodes)
    assert category_root_nodes_counts == 4

    assert test_category not in category_root_nodes


def test_destroy_admin_nonexistent_category_node_delete_api_return_error(
    api_client: 'APIClient'
) -> None:

    """
    Test delete category node for a category that does not exist.

    This test verifies that when the client attempts to delete a category
    using a not existed category slug, the API responds with
    an 'HTTP 404 Not Found' error.

    The test constructs a URL for the category endpoint using a not existed category
    slug and sends a DELETE request to this URL. The test expects the API to respond
    with an HTTP 404 status code indicating that the category with the specified
    slug was not found.

    :param api_client: An instance of the Django REST Framework's APIClient.

    :return: None
    """

    not_exists_category_slug = 'not-exists-category-slug'

    url = category_admin_node_url(
        category_slug=not_exists_category_slug,
    )

    response = api_client.delete(path=url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
