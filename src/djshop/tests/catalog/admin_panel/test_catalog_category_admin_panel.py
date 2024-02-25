from typing import TYPE_CHECKING

import pytest
from django.urls import reverse
from rest_framework import status


if TYPE_CHECKING:
    from django.test import Client

    from src.djshop.catalog.models import Category
    from src.djshop.users.models import BaseUser


pytestmark = pytest.mark.django_db


ADMIN_PANEL_CATEGORY_OBJECT_LIST_URL = reverse(
    viewname='admin:catalog_category_changelist'
)

ADMIN_PANEL_CATEGORY_OBJECT_ADD_URL = reverse(
    viewname='admin:catalog_category_add'
)


def admin_panel_category_object_update_url(category_id: int) -> str:

    """
    Generate URL for updating a category object in the admin panel.

    :param category_id: The ID of the category object.
    :return: The URL for updating the category object.
    """

    return reverse(
        viewname='admin:catalog_category_change', args=[category_id]
    )


def admin_panel_category_object_delete_url(category_id: int) -> str:

    """
    Generate URL for deleting a category object in the admin panel.

    :param category_id: The ID of the category object.
    :return: The URL for deleting the category object.
    """

    return reverse(
        viewname='admin:catalog_category_delete', args=[category_id]
    )


def test_catalog_category_admin_panel_list_display_view(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_root_category: 'Category'
) -> None:

    """
    Test the list display view of the Category admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_root_category: Category instance to be displayed.
    """

    client.force_login(user=first_test_superuser)
    response = client.get(path=ADMIN_PANEL_CATEGORY_OBJECT_LIST_URL)

    # Check if the response status is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Check if the category title is present in the response content
    test_category_title = first_test_root_category.title
    assert bytes(test_category_title, 'utf-8') in response.content

    # Check if the is_public field value is present in the response content
    test_category_publication = first_test_root_category.is_public
    assert str(test_category_publication) in response.content.decode()


def test_category_admin_panel_search_fields_list_display_view(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_root_category: 'Category'
) -> None:

    """
    Test the list display view search fields of the Category admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_root_category: Category instance to be displayed.
    """

    client.force_login(user=first_test_superuser)

    search_input = first_test_root_category.title
    response = client.get(
        path=ADMIN_PANEL_CATEGORY_OBJECT_LIST_URL,
        data={'q': search_input}
    )

    # Check if the response status is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Check if the option grou[ title is present in the response content
    test_option_group_title = first_test_root_category.title
    assert test_option_group_title in response.content.decode()


def test_category_admin_panel_add_object_view(
        client: 'Client', first_test_superuser: 'BaseUser',
) -> None:

    """
    Test the "add" object view of the Category admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    """

    client.force_login(first_test_superuser)
    response = client.get(path=ADMIN_PANEL_CATEGORY_OBJECT_ADD_URL)
    assert response.status_code == status.HTTP_200_OK


def test_category_admin_panel_update_object_view(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_root_category: 'Category'
) -> None:

    """
    Test the update object view of the Category admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_root_category: Category instance to be updated.
    """

    client.force_login(first_test_superuser)
    url = admin_panel_category_object_update_url(
        category_id=first_test_root_category.pk
    )
    response = client.get(path=url)
    assert response.status_code == status.HTTP_200_OK


def test_category_admin_panel_delete_object_view(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_root_category: 'Category'
) -> None:

    """
    Test the "delete" object view of the Category admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_root_category: Category instance to be deleted.
    """

    client.force_login(first_test_superuser)
    url = admin_panel_category_object_delete_url(
        category_id=first_test_root_category.pk
    )
    response = client.get(path=url)
    assert response.status_code == status.HTTP_200_OK
