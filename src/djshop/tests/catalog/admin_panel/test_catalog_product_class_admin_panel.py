from typing import TYPE_CHECKING

import pytest
from django.urls import reverse
from rest_framework import status


if TYPE_CHECKING:
    from django.test import Client

    from src.djshop.catalog.models import Attribute, ProductClass
    from src.djshop.users.models import BaseUser


pytestmark = pytest.mark.django_db


ADMIN_PANEL_PRODUCT_CLASS_OBJECT_LIST_URL = reverse(
    viewname='admin:catalog_productclass_changelist'
)

ADMIN_PANEL_PRODUCT_CLASS_OBJECT_ADD_URL = reverse(
    viewname='admin:catalog_productclass_add'
)


def admin_panel_product_class_object_update_url(product_class_id: int) -> str:

    """
    Generate URL for updating a product_class object in the admin panel.

    :param product_class_id: The ID of the product class object.
    :return: The URL for updating the product class object.
    """

    return reverse(
        viewname='admin:catalog_productclass_change', args=[product_class_id]
    )


def admin_panel_product_class_object_delete_url(product_class_id: int) -> str:

    """
    Generate URL for deleting a product_class object in the admin panel.

    :param product_class_id: The ID of the product class object.
    :return: The URL for deleting the product class object.
    """

    return reverse(
        viewname='admin:catalog_productclass_delete', args=[product_class_id]
    )


def test_product_class_admin_panel_list_display_view(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_product_class: 'ProductClass',
        first_test_attribute: 'Attribute'
) -> None:

    """
    Test the list display view of the Product Class admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_product_class: Product Class instance to be displayed.
    """

    first_test_product_class.attributes.add(first_test_attribute)
    first_test_product_class.save()

    client.force_login(user=first_test_superuser)
    response = client.get(path=ADMIN_PANEL_PRODUCT_CLASS_OBJECT_LIST_URL)
    assert response.status_code == status.HTTP_200_OK

    response_content = response.content.decode()
    assert first_test_product_class.title in response_content
    assert str(first_test_product_class.require_shipping) in response_content

    product_class_attribute_count = len(first_test_product_class.attributes.all())
    assert product_class_attribute_count == 1
    assert str(product_class_attribute_count) in response_content


def test_product_class_admin_panel_list_display_view_search_fields(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_product_class: 'ProductClass',
) -> None:

    """
    Test the list display view search fields of the Product Class admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_product_class: Product Class instance to be displayed.
    """

    client.force_login(user=first_test_superuser)

    search_input = first_test_product_class.title
    response = client.get(
        path=ADMIN_PANEL_PRODUCT_CLASS_OBJECT_LIST_URL,
        data={'q': search_input}
    )

    # Check if the response status is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Check if the product class title is present in the response content
    test_product_class_title = first_test_product_class.title
    assert test_product_class_title in response.content.decode()


def test_product_class_admin_panel_add_object_view(
        client: 'Client', first_test_superuser: 'BaseUser',
) -> None:

    """
    Test the "add" object view of the Product Class admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    """

    client.force_login(first_test_superuser)
    response = client.get(path=ADMIN_PANEL_PRODUCT_CLASS_OBJECT_ADD_URL)
    assert response.status_code == status.HTTP_200_OK


def test_product_class_admin_panel_update_object_view(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_product_class: 'ProductClass'
) -> None:

    """
    Test the update object view of the Product Class admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_product_class: Product Class instance to be updated.
    """

    client.force_login(first_test_superuser)
    url = admin_panel_product_class_object_update_url(
        product_class_id=first_test_product_class.pk
    )
    response = client.get(path=url)
    assert response.status_code == status.HTTP_200_OK


def test_product_class_admin_panel_delete_object_view(
        client: 'Client', first_test_superuser: 'BaseUser',
        first_test_product_class: 'ProductClass'
) -> None:

    """
    Test the "delete" object view of the Product Class admin panel.

    :param client: Django test client.
    :param first_test_superuser: Superuser instance for authentication.
    :param first_test_product_class: Product Class instance to be deleted.
    """

    client.force_login(first_test_superuser)
    url = admin_panel_product_class_object_delete_url(
        product_class_id=first_test_product_class.pk
    )
    response = client.get(path=url)
    assert response.status_code == status.HTTP_200_OK
