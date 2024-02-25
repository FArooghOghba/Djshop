from typing import TYPE_CHECKING

import pytest
from django.urls import reverse
from rest_framework import status


if TYPE_CHECKING:
    from django.test import Client

    from src.djshop.catalog.models import OptionGroup
    from src.djshop.users.models import BaseUser


pytestmark = pytest.mark.django_db


ADMIN_PANEL_OPTION_GROUP_OBJECT_LIST_URL = reverse(
    viewname='admin:catalog_optiongroup_changelist'
)

ADMIN_PANEL_OPTION_GROUP_OBJECT_ADD_URL = reverse(
    viewname='admin:catalog_optiongroup_add'
)


def admin_panel_option_group_object_update_url(option_group_id: int) -> str:

    """
    Generate URL for updating an option group object in the admin panel.

    :param option_group_id: The ID of the option group object.
    :return: The URL for updating the option group object.
    """

    return reverse(
        viewname='admin:catalog_optiongroup_change', args=[option_group_id]
    )


def admin_panel_option_group_object_delete_url(option_group_id: int) -> str:

    """
    Generate URL for deleting an option_group object in the admin panel.

    :param option_group_id: The ID of the option group object.
    :return: The URL for deleting the option group object.
    """

    return reverse(
        viewname='admin:catalog_optiongroup_delete', args=[option_group_id]
    )


def test_option_group_admin_panel_list_display_view(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_option_group: 'OptionGroup'
) -> None:

    """
    Test the list display view of the Option Group admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_option_group: Option Group instance to be displayed.
    """

    client.force_login(user=first_test_superuser)
    response = client.get(path=ADMIN_PANEL_OPTION_GROUP_OBJECT_LIST_URL)

    # Check if the response status is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Check if the option grou[ title is present in the response content
    test_option_group_title = first_test_option_group.title
    assert test_option_group_title in response.content.decode()


def test_option_group_admin_panel_search_fields_list_display_view(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_option_group: 'OptionGroup'
) -> None:

    """
    Test the list display view search fields of the Option Group admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_option_group: Option Group instance to be displayed.
    """

    client.force_login(user=first_test_superuser)

    search_input = first_test_option_group.title
    response = client.get(
        path=ADMIN_PANEL_OPTION_GROUP_OBJECT_LIST_URL,
        data={'q': search_input}
    )

    # Check if the response status is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Check if the option grou[ title is present in the response content
    test_option_group_title = first_test_option_group.title
    assert test_option_group_title in response.content.decode()


def test_option_group_admin_panel_add_object_view(
        client: 'Client', first_test_superuser: 'BaseUser',
) -> None:

    """
    Test the "add" object view of the Option Group admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    """

    client.force_login(first_test_superuser)
    response = client.get(path=ADMIN_PANEL_OPTION_GROUP_OBJECT_ADD_URL)
    assert response.status_code == status.HTTP_200_OK


def test_option_group_admin_panel_update_object_view(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_option_group: 'OptionGroup'
) -> None:

    """
    Test the update object view of the Option Group admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_option_group: Option Group instance to be updated.
    """

    client.force_login(first_test_superuser)
    url = admin_panel_option_group_object_update_url(
        option_group_id=first_test_option_group.pk
    )
    response = client.get(path=url)
    assert response.status_code == status.HTTP_200_OK


def test_option_group_admin_panel_delete_object_view(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_option_group: 'OptionGroup'
) -> None:

    """
    Test the "delete" object view of the Category admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_option_group: Option Group instance to be deleted.
    """

    client.force_login(first_test_superuser)
    url = admin_panel_option_group_object_delete_url(
        option_group_id=first_test_option_group.pk
    )
    response = client.get(path=url)
    assert response.status_code == status.HTTP_200_OK
