from typing import TYPE_CHECKING, cast

import pytest

from src.djshop.tests.factories.catalog_factories import CategoryFactory


if TYPE_CHECKING:
    from src.djshop.catalog.models import Category


@pytest.fixture
def first_test_root_category() -> 'Category':

    """
    Pytest fixture that creates and returns a root Category instance
    using CategoryFactory.

    This fixture uses the factory_boy library to generate a root Category
    instance with random data for the 'name' and 'description' fields.
    The instance is saved to the test database.

    :returns: Category: A Category instance with random data.
    """

    test_category = CategoryFactory()
    return cast('Category', test_category)


@pytest.fixture
def second_test_root_category() -> 'Category':

    """
    Pytest fixture that creates and returns a root Category instance
    using CategoryFactory.

    This fixture uses the factory_boy library to generate a Category
    instance with random data for the 'name' and 'description' fields.
    The instance is saved to the test database.

    :returns: Category: A Category instance with random data.
    """

    test_category = CategoryFactory()
    return cast('Category', test_category)
