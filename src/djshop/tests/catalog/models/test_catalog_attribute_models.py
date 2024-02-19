import pytest

from src.djshop.catalog.models import Attribute, OptionGroup, ProductClass


pytestmark = pytest.mark.django_db


def test_create_attribute_return_success(
    first_test_product_class: 'ProductClass'
) -> None:

    """
    Test the creation of an Attribute without an OptionGroup.
    Asserts that the created Attribute has the correct properties.

    :param first_test_product_class: A fixture providing the product class instance.
    :return: None
    """

    test_attribute_title = "Test Attribute"
    test_attribute = Attribute.objects.create(
        product_class=first_test_product_class, title=test_attribute_title
    )

    get_attribute = Attribute.objects.get(pk=test_attribute.id)
    assert get_attribute.product_class == first_test_product_class
    assert get_attribute.title == test_attribute_title
    assert get_attribute.type == 'text'
    assert get_attribute.required is False


def test_create_attribute_with_option_group_return_success(
        first_test_product_class: 'ProductClass',
        first_test_option_group: 'OptionGroup'
) -> None:

    """
    Test the creation of an Attribute with an OptionGroup.
    Asserts that the created Attribute is linked to the correct OptionGroup.

    :param first_test_product_class: A fixture providing the product class instance.
    :param first_test_option_group: A fixture providing the option group queryset.
    :return: None
    """

    test_attribute_title = "Test Attribute"
    test_attribute = Attribute.objects.create(
        product_class=first_test_product_class,
        title=test_attribute_title,
        option_group=first_test_option_group
    )

    get_attribute = Attribute.objects.get(pk=test_attribute.id)
    assert get_attribute.option_group == first_test_option_group


def test_create_attribute_without_option_group_return_success(
        first_test_product_class: 'ProductClass'
) -> None:

    """
    Test the creation of an Attribute without an OptionGroup.
    Asserts that the created Attribute is not linked to any OptionGroup.

    :param first_test_product_class: A fixture providing the product class instance.
    :return: None
    """

    test_attribute_title = "Test Attribute"
    test_attribute = Attribute.objects.create(
        product_class=first_test_product_class, title=test_attribute_title
    )

    get_attribute = Attribute.objects.get(pk=test_attribute.id)
    assert get_attribute.option_group is None
