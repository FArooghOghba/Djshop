from typing import TYPE_CHECKING, cast

import pytest

from src.djshop.tests.factories.product_class_factories import (
    AttributeFactory, OptionGroupFactory, OptionGroupValuesFactory,
    ProductClassFactory,
)


if TYPE_CHECKING:
    from src.djshop.catalog.models import (
        Attribute, OptionGroup, OptionGroupValues, ProductClass,
    )


@pytest.fixture
def first_test_product_class() -> 'ProductClass':

    """
    Pytest fixture that creates and returns a Product class instance
    using ProductClassFactory.

    This fixture uses the factory_boy library to generate a Product Class
    instance with random data for the 'title' and 'description' fields.
    The instance is saved to the test database.

    :returns: ProductClass: A Product Class instance with random data.
    """

    test_product_class = ProductClassFactory()
    return cast('ProductClass', test_product_class)


@pytest.fixture
def first_test_option_group() -> 'OptionGroup':

    """
    Fixture for creating a test option group.

    This fixture creates and returns a test option group object using
    the `OptionGroupFactory`.

    :return: OptionGroup: A test option group object.
    """

    test_option_group = OptionGroupFactory()
    return cast('OptionGroup', test_option_group)


@pytest.fixture
def first_test_attribute() -> 'Attribute':

    """
    Fixture for creating a test attribute.

    This fixture creates and returns a test attribute object using
    the `AttributeFactory`.

    :return: Attribute: A test attribute object.
    """

    test_attribute = AttributeFactory()
    return cast('Attribute', test_attribute)


@pytest.fixture
def first_test_option_group_values() -> 'OptionGroupValues':

    """
    Fixture for creating a test option group values.

    This fixture creates and returns a test "option group values" object using
    the `OptionGroupValuesFactory`.

    :return: OptionGroupValues: A test option group values object.
    """

    return cast('OptionGroupValues', OptionGroupValuesFactory)
