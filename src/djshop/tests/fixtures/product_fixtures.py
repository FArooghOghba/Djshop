from typing import TYPE_CHECKING, cast

import pytest

from src.djshop.tests.factories.product_factories import ProductFactory


if TYPE_CHECKING:
    from src.djshop.catalog.models import Product


@pytest.fixture
def first_test_product() -> 'Product':

    """
    Pytest fixture that creates and returns a Product instance
    using ProductFactory.

    This fixture uses the factory_boy library to generate a Product
    instance with random data for the 'title' and 'description' fields.
    The instance is saved to the test database.

    :returns: Product: A Product instance with random data.
    """

    test_product = ProductFactory()
    return cast('Product', test_product)


@pytest.fixture
def second_test_product() -> 'Product':

    """
    Pytest fixture that creates and returns a Product instance
    using ProductFactory.

    This fixture uses the factory_boy library to generate a Product
    instance with random data for the 'title' and 'description' fields.
    The instance is saved to the test database.

    :returns: Product: A Product instance with random data.
    """

    test_product = ProductFactory()
    return cast('Product', test_product)


@pytest.fixture
def third_test_product() -> 'Product':

    """
    Pytest fixture that creates and returns a Product instance
    using ProductFactory.

    This fixture uses the factory_boy library to generate a Product
    instance with random data for the 'title' and 'description' fields.
    The instance is saved to the test database.

    :returns: Product: A Product instance with random data.
    """

    test_product = ProductFactory()
    return cast('Product', test_product)
