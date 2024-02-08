from typing import TYPE_CHECKING

import pytest
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


@pytest.mark.parametrize(
    'field_key, field_value', (
        ['title', 'First Test Edited Category'],
        ['description', 'This is the edited category.'],
        ['is_public', False]
    )
)
def test_update_admin_category_node_patch_api_return_success(
    api_client: 'APIClient', first_test_root_category: 'Category',
    field_key: str, field_value: str
) -> None:

    """
    Test that updating a category node through the admin PATCH API using
    the PATCH method is successful.

    This test ensures that a user can successfully update the details
    of a category node by sending a PATCH request to the category admin
    node API endpoint with the updated payload.

    :param api_client: A fixture providing the Django test client for
    API requests.
    :param first_test_root_category: A fixture providing the first test
    root category object.
    :param field_key: A parameter representing category object field.
    :param field_value: A parameter representing category object field value.

    :return: None
    """

    fields = ('title', 'description', 'is_public')

    # Update the category node with new category values.
    payload = {
        field_key: field_value
    }
    url = category_admin_node_url(category_slug=first_test_root_category.slug)
    category_update_response = api_client.patch(
        path=url, data=payload
    )
    assert category_update_response.status_code == status.HTTP_202_ACCEPTED

    # Assert that the updated details match the expected values.
    test_category_after_update_res = category_update_response.data
    assert test_category_after_update_res[field_key] == payload[field_key]

    # Assert that the details before the update are different from
    # the updated values.
    for field in fields:
        if field != field_key:
            field_after_update = getattr(first_test_root_category, field)
            assert test_category_after_update_res[field] == field_after_update


def test_update_admin_nonexistent_category_node_patch_api_return_error(
    api_client: 'APIClient',
) -> None:

    """
    Test update a category node that does not exist.

    This test verifies that when the client attempts to update a category
    node using a not existed category slug, the API responds with
    an 'HTTP 404 Not Found' error.

    The test constructs a URL for the category node endpoint using a not
    existed category slug and sends a PATCH request to this URL with a valid
    payload containing the category data. The test expects the API to respond
    with an HTTP 404 status code indicating that the category with the specified
    slug was not found.

    :param api_client: An instance of the Django REST Framework's APIClient.
    :return: None
    """

    not_exists_category_slug = 'not-exists-category-slug'

    url = category_admin_node_url(category_slug=not_exists_category_slug)
    payload = {
        'title': 'First Test Edited Category',
    }

    response = api_client.patch(path=url, data=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    'wrong_title, error_message', (
        ['', 'This field may not be blank.'],
        [' ', 'This field may not be blank.'],
        ['6char', 'title must include at least 6 letters']
    )
)
def test_update_admin_wrong_data_category_node_patch_api_return_error(
    api_client: 'APIClient', first_test_root_category: 'Category',
    wrong_title: str, error_message: str
) -> None:

    """
     Test that PATCH a category with wrong data returns a 400 Bad Request error.

    This parameterized test checks various cases where the provided category data
    is invalid, such as wrong title format, min letters, empty string,
    or white-space.

    The test ensures that the API returns a 400 Bad Request status for each
    invalid case.

    :param api_client: An instance of the Django REST Framework's APIClient.
    :param first_test_root_category: A fixture providing the first test
    category object.
    :param wrong_title: A parameter representing invalid title values.
    :param error_message: A parameter representing error message.
    :return: None
    """

    url = category_admin_node_url(category_slug=first_test_root_category.slug)
    payload = {
        'title': wrong_title,
    }

    response = api_client.patch(path=url, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['title'][0] == error_message


def test_update_admin_category_node_with_duplicate_title_patch_api_return_error(
        api_client: 'APIClient', first_test_root_category: 'Category',
        second_test_root_category: 'Category'
) -> None:

    """
    Test that the PATCH API returns an error when trying to update a category
    node with a title that already exists.

    :param api_client: An instance of the Django REST Framework's APIClient.
    :param first_test_root_category: A category instance created for testing.
    :param second_test_root_category: A category instance created for testing.

    :return: None
    """

    duplicate_title = first_test_root_category.title

    # This payload includes a 'title' field that already exists in the database
    url = category_admin_node_url(category_slug=second_test_root_category.slug)
    payload = {
        'title': duplicate_title,
    }
    response = api_client.patch(path=url, data=payload)

    # Check that the API returned a 400 Bad Request status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Check that the error message in the response data is correct
    assert response.data['message'] == 'Validation error'

    response_error = response.data['extra']['fields']
    assert response_error['title'][0] == 'Category with this Title already exists.'
