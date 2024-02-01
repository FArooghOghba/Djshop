from typing import TYPE_CHECKING, Dict, Generator, cast

import pytest

from src.djshop.tests.factories.category_factories import CategoryFactory


if TYPE_CHECKING:
    from factory import LazyAttribute

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
def five_test_root_categories() -> Generator['Category', None, None]:

    """
    Fixture that creates a batch of five test root categories.

    This fixture uses the CategoryFactory to create a batch of five
    test root categories and yields the created categories.
    The test categories can be used in tests that require multiple
    category objects.

    :return: A list of five test category objects.
    """

    test_movies = CategoryFactory.create_batch(5)
    yield cast('Category', test_movies)


@pytest.fixture
def first_test_category_payload() -> Dict[str, 'LazyAttribute']:

    """
    Fixture for creating a test category instance.

    This fixture uses the `CategoryFactory`
    to create a test category instance. The created category
    can be used in tests to simulate a category with predefined
    attributes for testing various scenarios.

    :return: a dict test category payload
    """

    return CategoryFactory.create_payload()


@pytest.fixture
def second_test_category_payload() -> Dict[str, 'LazyAttribute']:

    """
    Fixture for creating a test category instance.

    This fixture uses the `CategoryFactory`
    to create a test category instance. The created category
    can be used in tests to simulate a category with predefined
    attributes for testing various scenarios.

    :return: a dict test category payload
    """

    return CategoryFactory.create_payload()
