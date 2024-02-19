from typing import TYPE_CHECKING, cast

import pytest

from src.djshop.tests.factories.product_class_factories import ProductClassFactory


if TYPE_CHECKING:
    from src.djshop.catalog.models import ProductClass


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
