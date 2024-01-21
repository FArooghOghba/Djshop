from typing import TYPE_CHECKING, Generator, cast

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


@pytest.fixture
def five_test_categories() -> Generator['Category', None, None]:

    """
    Fixture that creates a batch of five test categories.

    This fixture uses the CategoryFactory to create a batch of five test categories
    and yields the created categories. The test categories can be used in tests that
    require multiple category objects.

    :return: A list of five test category objects.
    """

    test_movies = CategoryFactory.build_batch(5)
    yield cast('Category', test_movies)
