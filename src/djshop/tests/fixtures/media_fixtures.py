from typing import TYPE_CHECKING, cast

import pytest

from src.djshop.tests.factories.media_factories import ImageFactory


if TYPE_CHECKING:
    from src.djshop.media.models import Image


@pytest.fixture
def first_test_image() -> 'Image':

    """
    Pytest fixture that creates and returns an Image instance
    using ImageFactory.

    This fixture uses the factory_boy library to generate an Image
    instance with random data, The instance is saved to the test database.

    :returns: Image: An Image instance with random data.
    """

    test_image = ImageFactory()
    return cast('Image', test_image)


@pytest.fixture
def second_test_image() -> 'Image':

    """
    Pytest fixture that creates and returns an Image instance
    using ImageFactory.

    This fixture uses the factory_boy library to generate an Image
    instance with random data, The instance is saved to the test database.

    :returns: Image: An Image instance with random data.
    """

    test_image = ImageFactory()
    return cast('Image', test_image)


@pytest.fixture
def third_test_image() -> 'Image':

    """
    Pytest fixture that creates and returns an Image instance
    using ImageFactory.

    This fixture uses the factory_boy library to generate an Image
    instance with random data, The instance is saved to the test database.

    :returns: Image: An Image instance with random data.
    """

    test_image = ImageFactory()
    return cast('Image', test_image)
