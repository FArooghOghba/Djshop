from typing import TYPE_CHECKING, cast

import pytest

from src.djshop.tests.factories.attribute_factories import AttributeFactory


if TYPE_CHECKING:
    from src.djshop.catalog.models import Attribute


@pytest.fixture
def first_test_attribute() -> 'Attribute':

    """
    Pytest fixture that creates and returns an Attribute instance
    using AttributeFactory.

    This fixture uses the factory_boy library to generate an Attribute
    instance with random data for the 'title' field.
    The instance is saved to the test database.

    :returns: Product: An Attribute instance with random data.
    """

    test_attribute = AttributeFactory()
    return cast('Attribute', test_attribute)


@pytest.fixture
def second_test_attribute() -> 'Attribute':

    """
    Pytest fixture that creates and returns an Attribute instance
    using AttributeFactory.

    This fixture uses the factory_boy library to generate an Attribute
    instance with random data for the 'title' field.
    The instance is saved to the test database.

    :returns: Product: An Attribute instance with random data.
    """

    test_attribute = AttributeFactory()
    return cast('Attribute', test_attribute)
