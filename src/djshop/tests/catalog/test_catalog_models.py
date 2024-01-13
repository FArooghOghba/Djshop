import pytest
from django.core.exceptions import ValidationError

from src.djshop.catalog.models import Category


pytestmark = pytest.mark.django_db


def test_create_root_category_return_success() -> None:

    """
    Test the creation of a root category and verify the success of the operation.

    This test function performs the following steps:
    1. Create a root category with specified title and description.
    2. Check if the category is saved correctly in the database.
    3. Retrieves the category object from the database and verifies its attributes.
    4. Validates the materialized path attributes (depth and path).
    :return: None
    """

    test_category_title = 'test root category title'
    test_category_description = 'test root category descriptions.'

    test_category = Category.add_root(
        title=test_category_title,
        description=test_category_description
    )

    # Check if the category was saved correctly
    test_category_counts = Category.objects.count()
    assert test_category_counts == 1

    get_test_category_object = Category.objects.get(slug=test_category.slug)
    get_test_category_title = get_test_category_object.title
    assert get_test_category_title == test_category_title

    assert str(test_category) == test_category.title
    assert test_category.description == test_category_description
    assert test_category.is_public is True

    # Check the materialized path (depth, path)
    assert test_category.get_depth() == 1
    assert test_category.path


def test_create_child_category_return_success(
    first_test_root_category: 'Category'
) -> None:

    """
    Test the creation of a child category and verify the success of the operation.

    This test function depends on the existence of a root category
    provided as a fixture.

    It performs the following steps:
    1. Creates a child category for the provided root category.
    2. Check if the child category is saved correctly in the database.
    3. Retrieves the child category object from the database and
        verifies its attributes.
    4. Validates the materialized path attributes of the child
        category (depth and path).

    :params: first_test_root_category ('Category'): A fixture providing
            the root category.
    :return: None
    """

    test_child_category_title = 'First Test Child Category'

    first_test_child_category = first_test_root_category.add_child(
        title=test_child_category_title,
        description='This is the first test child for this category.'
    )

    # Check if the child category was saved correctly
    test_category_counts = Category.objects.count()
    assert test_category_counts == 2

    get_test_child_category_object = Category.objects.get(
        slug=first_test_child_category.slug
    )
    get_test_child_category_title = get_test_child_category_object.title
    assert get_test_child_category_title == test_child_category_title

    # Check the materialized path of the child (depth, path)
    assert first_test_child_category.get_depth() == 2
    assert first_test_child_category.path


def test_create_root_category_with_empty_title_return_error(
    first_test_root_category: 'Category'
) -> None:

    """
    Test that creating a root category with an empty title raises
    a validation error.

    This test sets an empty title on the first_test_root_category
    fixture object and calls the full_clean() method. It expects a
    ValidationError to be raised.

    :param first_test_root_category: A fixture providing the test
    root category object.
    :return: None
    """

    test_category = first_test_root_category
    test_category.title = ''  # Empty title

    with pytest.raises(ValidationError):
        test_category.full_clean()


def test_create_root_category_with_exists_title_return_error(
    first_test_root_category: 'Category', second_test_root_category: 'Category'
) -> None:

    """
    Test that creating a root category with an existing title raises
    a validation error.

    This test sets the title of the first_test_root_category fixture object
    to the title of the second_test_root_category fixture object, creating
    a case where the title already exists. It then calls the full_clean()
    method and expects a ValidationError to be raised.

    :param first_test_root_category: A fixture providing the first test
    root category object.
    :param second_test_root_category: A fixture providing the second test
    root category object.
    :return: None
    """

    test_category = first_test_root_category
    test_category.title = second_test_root_category.title  # Exists title

    with pytest.raises(ValidationError):
        test_category.full_clean()
