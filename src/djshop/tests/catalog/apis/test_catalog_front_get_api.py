from typing import TYPE_CHECKING

import pytest
from django.urls import reverse
from rest_framework import status

from src.djshop.catalog.selectors.category import get_category_detail


if TYPE_CHECKING:
    from rest_framework.test import APIClient

    from src.djshop.catalog.models import Category


pytestmark = pytest.mark.django_db


def category_detail_url(category_slug: str) -> str:

    """
    Generate the URL for the category detail API endpoint based on the category slug.

    This function takes a category slug as input and generates the URL for the
    movie detail API endpoint by using the `reverse` function provided by Django's
    URL resolver. The category slug is included as a parameter in the URL.

    :param category_slug: The slug of the category.
    :return: The URL for the category 'detail API' endpoint.
    """

    return reverse(viewname='api:catalog:category-detail', args=[category_slug])


def test_get_category_detail_return_success(
    api_client: 'APIClient', first_test_root_category: 'Category',
) -> None:

    """
    Test that retrieving movie details for a user should succeed.

    This test ensures that a user can retrieve the details of a category
    through the API. 'api_client.get()' method is used to perform the GET
    request for movie details.

    :param first_test_root_category: A fixture providing the first test root
                                    category object.

    :return: None
    """

    first_test_category_slug = first_test_root_category.slug

    url = category_detail_url(category_slug=first_test_category_slug)

    response = api_client.get(path=url)
    assert response.status_code == status.HTTP_200_OK

    # Assertion: Check that the average rating is calculated correctly for the movie
    test_category = get_category_detail(category_slug=first_test_category_slug)
    test_category_title = test_category.title
    assert response.data['title'] == test_category_title


def test_get_nonexistent_category_detail_return_error(
    api_client: 'APIClient'
) -> None:

    """
    Test retrieving details of a nonexistent category.

    This test verifies that when requesting the details of a category
    that does not exist, the API returns a not found error.

    :param api_client: A fixture providing the Django test client for API requests.

    :return: None
    """

    url = category_detail_url(category_slug='nonexistent-slug')
    response = api_client.get(path=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
