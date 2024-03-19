from typing import TYPE_CHECKING

import pytest
from django.db import IntegrityError

from src.djshop.catalog.models import Image, Product, Recommendations


if TYPE_CHECKING:
    from src.djshop.catalog.models import Attribute, ProductClass
    from src.djshop.media.models import Image as MediaImage


pytestmark = pytest.mark.django_db


def test_create_product_return_success() -> None:

    """
    Test creating a Product instance.
    """

    test_product_title = "Test Product Title"
    test_product = Product.objects.create(
        title=test_product_title,
    )

    # Check if the category was saved correctly
    test_product_counts = Product.objects.count()
    assert test_product_counts == 1

    get_product = Product.objects.get(slug=test_product.slug)
    assert get_product.structure == 'standalone'
    assert get_product.title == test_product_title

    # Ensure slug is generated correctly
    assert get_product.slug == "test-product-title"
    assert get_product.is_public is True
    assert get_product.main_image is None


def test_create_product_with_parent_return_success(
        first_test_product: "Product"
) -> None:

    """
    Test creating a Product instance with a parent.

    :param first_test_product: The parent Product instance.
    """

    test_product = Product.objects.create(
        structure='parent',
        title="Test Product Title",
        parent=first_test_product
    )

    get_product = Product.objects.get(slug=test_product.slug)

    # Check if the category was saved correctly
    test_product_counts = Product.objects.count()
    assert test_product_counts == 2
    assert get_product.structure == 'parent'


def test_create_product_with_product_class_return_success(
        first_test_product_class: "ProductClass"
) -> None:

    """
    Test creating a Product instance with a product class.

    :param first_test_product_class: The ProductClass instance.
    """

    test_product = Product.objects.create(
        title="Test Product Title",
        product_class=first_test_product_class
    )

    get_product = Product.objects.get(slug=test_product.slug)

    # Check if the category was saved correctly
    test_product_counts = Product.objects.count()
    assert test_product_counts == 1
    assert get_product.product_class
    assert get_product.product_class.title == first_test_product_class.title


def test_create_product_with_attributes_return_success(
        first_test_attribute: "Attribute", second_test_attribute: 'Attribute'
) -> None:

    """
    Test creating a Product instance with attributes.

    :param first_test_attribute: The first Attribute instance.
    :param second_test_attribute: The second Attribute instance.
    """

    test_product = Product.objects.create(
        title="Test Product Title",
    )
    test_product.attributes.add(first_test_attribute, second_test_attribute)

    get_product = Product.objects.get(slug=test_product.slug)

    # Check if the product has the correct attributes
    assert get_product.attributes.count() == 2

    all_test_product_attributes = get_product.attributes.all()
    assert first_test_attribute in all_test_product_attributes
    assert second_test_attribute in all_test_product_attributes


def test_create_product_with_duplicate_attributes_return_error(
        first_test_product: "Product", first_test_attribute: "Attribute",
) -> None:

    """
    Test creating a Product instance with duplicate attributes.

    :param first_test_product: The Product instance.
    :param first_test_attribute: The Attribute instance.
    """

    first_test_product.attributes.add(first_test_attribute)

    # Try adding the same attribute again
    first_test_product.attributes.add(first_test_attribute)

    # Assert that the attribute was not added again
    # Check if the product has the correct attributes
    get_product = Product.objects.get(slug=first_test_product.slug)
    assert get_product.attributes.count() == 1


def test_create_product_with_recommendations_return_success(
        first_test_product: "Product", second_test_product: "Product",
        third_test_product: "Product"
) -> None:

    """
    Test creating a Product instance with recommendations.

    :param first_test_product: The Product instance.
    :param second_test_product: The first recommended Product instance.
    :param third_test_product: The second recommended Product instance.
    """

    # Add recommendations
    Recommendations.objects.create(
        primary=first_test_product, normal=second_test_product, rank=1
    )
    Recommendations.objects.create(
        primary=first_test_product, normal=third_test_product, rank=2
    )

    # Check recommendations
    get_product = Product.objects.get(slug=first_test_product.slug)
    test_product_recommendations = list(get_product.recommendations.all())
    assert test_product_recommendations == [second_test_product, third_test_product]


def test_create_product_with_duplicate_recommendations_return_error(
        first_test_product: "Product", second_test_product: "Product",
) -> None:

    """
    Test creating a Product instance with duplicate recommendations.

    :param first_test_product: The Product instance.
    :param second_test_product: The recommended Product instance.
    """

    # Add duplicate recommendation
    Recommendations.objects.create(
        primary=first_test_product, normal=second_test_product, rank=1
    )

    # Try adding the same recommendation again
    with pytest.raises(IntegrityError):
        Recommendations.objects.create(
            primary=first_test_product, normal=second_test_product, rank=2
        )


def test_create_product_with_recommendations_ordering_return_success(
        first_test_product: "Product", second_test_product: "Product",
        third_test_product: "Product"
) -> None:

    """
    Test creating a Product instance with 'recommendations' ordering.

    :param first_test_product: The Product instance.
    :param second_test_product: The first recommended Product instance.
    :param third_test_product: The second recommended Product instance.
    """

    # Add recommendations with different ranks
    Recommendations.objects.create(
        primary=first_test_product, normal=second_test_product, rank=2
    )
    Recommendations.objects.create(
        primary=first_test_product, normal=third_test_product, rank=1
    )

    # Check the order of recommendations
    get_product = Product.objects.get(slug=first_test_product.slug)
    first_test_product_recommendations = list(get_product.recommendations.all())
    test_recommendation_products = [second_test_product, third_test_product]
    assert first_test_product_recommendations == test_recommendation_products


def test_create_product_with_main_image_exists_return_success(
        first_test_product: "Product", first_test_image: "MediaImage",
        second_test_image: "MediaImage"
) -> None:

    """
    Test creating a Product instance with existing main image.

    :param first_test_product: The Product instance.
    :param first_test_image: The first MediaImage instance.
    :param second_test_image: The second MediaImage instance.
    """

    # Create images for the product
    first_test_product_image = Image.objects.create(
        product=first_test_product,
        image=first_test_image
    )

    Image.objects.create(
        product=first_test_product,
        image=second_test_image,
        display_order=1
    )

    # Check if the main image exists and is correct
    assert first_test_product.main_image == first_test_product_image


def test_update_product_main_image_after_delete_return_success(
        first_test_product: "Product", first_test_image: "MediaImage",
        second_test_image: "MediaImage", third_test_image: "MediaImage"
) -> None:

    """
    Test updating the main image of a Product instance after
    deleting the current main image.

    :param first_test_product: The Product instance.
    :param first_test_image: The first MediaImage instance.
    :param second_test_image: The second MediaImage instance.
    :param third_test_image: The third MediaImage instance.
    """

    # Create multiple images for the product
    first_test_product_image = Image.objects.create(
        product=first_test_product,
        image=first_test_image,
    )

    second_test_product_image = Image.objects.create(
        product=first_test_product,
        image=second_test_image,
        display_order=1
    )

    Image.objects.create(
        product=first_test_product,
        image=third_test_image,
        display_order=2
    )

    # Check if the main image exists and is correct
    assert first_test_product.main_image == first_test_product_image

    # Delete the main image and check again for the main image of the product.
    first_test_product_image.delete()
    assert first_test_product.main_image == second_test_product_image
