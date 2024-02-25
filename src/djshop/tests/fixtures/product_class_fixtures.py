from typing import TYPE_CHECKING, cast

import pytest

from src.djshop.tests.factories.product_class_factories import (
    OptionGroupFactory, OptionGroupValuesFactory, ProductClassFactory,
)


if TYPE_CHECKING:
    from src.djshop.catalog.models import OptionGroup, ProductClass


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
    the `OptionGroupFactory` factory.

    :return: Review: A test option group object.
    """

    return cast('OptionGroup', OptionGroupFactory)


@pytest.fixture
def first_test_option_group_values() -> 'OptionGroupValuesFactory':

    """
    Fixture for creating a test option group values.

    This fixture creates and returns a test "option group values" object using
    the `OptionGroupValuesFactory` factory.

    :return: Review: A test option group values object.
    """

    return OptionGroupValuesFactory()
