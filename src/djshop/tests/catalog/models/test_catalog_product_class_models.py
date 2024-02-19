import pytest
from django.db import IntegrityError

from src.djshop.catalog.models import Option, ProductClass


pytestmark = pytest.mark.django_db


def test_create_product_class_return_success() -> None:

    """
    Test creating a ProductClass instance.
    """

    test_product_class_title = "Test Product Class"
    test_product_description = 'test product descriptions.'

    test_product_class = ProductClass.objects.create(
        title=test_product_class_title,
        description=test_product_description
    )

    # Check if the category was saved correctly
    test_product_counts = ProductClass.objects.count()
    assert test_product_counts == 1

    get_product_class = ProductClass.objects.get(slug=test_product_class.slug)
    assert get_product_class.title == test_product_class_title

    # Ensure slug is generated correctly
    assert get_product_class.slug == "test-product-class"
    assert get_product_class.description == test_product_description
    assert get_product_class.require_shipping is True
    assert get_product_class.track_stock is True

    # Ensure initially no attributes exist
    assert not get_product_class.has_attributes()


def test_create_product_class_with_duplicate_title_return_error(
    first_test_product_class: 'ProductClass'
) -> None:

    """
    Test attempting to create a ProductClass instance with a duplicate title.

    :param first_test_product_class: A fixture providing the product class instance.
    :return: None
    """

    test_product_class_duplicate_title = first_test_product_class.title

    # Attempting to create a product class with duplicate title
    # should raise IntegrityError
    with pytest.raises(IntegrityError):
        ProductClass.objects.create(title=test_product_class_duplicate_title)


def test_create_product_class_with_unicode_title_return_success() -> None:

    """
    Test creating a ProductClass instance with a unicode title.
    """

    tes_product_class_title = "تست عنوان نمونه محصول"  # Unicode title
    test_product_class = ProductClass.objects.create(title=tes_product_class_title)

    get_product_class = ProductClass.objects.get(slug=test_product_class.slug)
    assert get_product_class.title == tes_product_class_title


def test_create_product_class_attribute_existence_return_success(
    first_test_product_class: 'ProductClass'
) -> None:

    """
    Test ensuring that attributes exist for a ProductClass instance after creation.

    :param first_test_product_class: A fixture providing the product class instance.
    :return: None
    """
    first_test_product_class.attributes.create(title="Test Attribute")

    # Ensure attributes exist after creation
    assert first_test_product_class.has_attributes()


def test_create_product_class_with_options_return_success(
        first_test_product_class: 'ProductClass', first_test_option: 'Option',
        second_test_option: 'Option'
) -> None:

    """
    Test associating options with a ProductClass instance.

    :param first_test_product_class: A fixture providing the product class instance.
    :param first_test_option: A fixture providing the option instance.
    :param second_test_option: A fixture providing the option instance.
    :return: None
    """

    # Add options to the product class
    first_test_product_class.option.add(first_test_option, second_test_option)
    first_test_product_class.save()

    # Retrieve the product class from the database
    retrieved_test_product_class = ProductClass.objects.get(
        slug=first_test_product_class.slug
    )

    # Ensure the options are associated with the product class
    assert retrieved_test_product_class.option.count() == 2

    test_product_class_options = retrieved_test_product_class.option.all()
    assert test_product_class_options.count() == 2
    assert first_test_option in test_product_class_options
    assert second_test_option in test_product_class_options
