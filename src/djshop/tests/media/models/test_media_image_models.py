import os
from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage  # type: ignore

from src.djshop.core.exceptions import DuplicateImageException
from src.djshop.media.models import Image, image_file_path


pytestmark = pytest.mark.django_db


@patch(target='src.djshop.media.models.uuid.uuid4')
def test_create_file_name_uuid_for_image_path(mock_uuid: 'MagicMock') -> None:

    """
    Test generating the image path for object images.

    This test mocks the UUID generation using the patch decorator
    to ensure a consistent UUID value. It calls the image_file_path()
    function with a fake file name. The expected file path is constructed
    based on UUID values. The test asserts that the generated file path
    matches the expected value.

    :param mock_uuid: A mock object for generating UUID values.
    :return: None
    """

    uuid = 'test_uuid'
    mock_uuid.return_value = uuid
    file_path = image_file_path(instance=None, filename='test-image.jpg')

    expected_file_path = os.path.normpath(f'uploads/images/{uuid}.jpg')

    assert file_path == expected_file_path


def sample_test_image_file(
        width: int = 100, height: int = 100
) -> 'SimpleUploadedFile':

    """
    Generates a test image file.

    This function creates a test image file
    and returns it as a SimpleUploadedFile object.

    :param: width (int): The width of the generated image. Default is 100.
    :param: height (int): The height of the generated image. Default is 100.

    returns: SimpleUploadedFile: A test image file.
    """

    # Create a new PIL Image with the specified dimensions
    image = PILImage.new(mode='RGB', size=(width, height))

    # Create a BytesIO object to hold the image data
    image_file = BytesIO()

    # Save the PIL Image to the BytesIO object as JPEG
    image.save(image_file, 'JPEG')

    # Seek back to the beginning of the BytesIO object
    image_file.seek(0)

    # Create a SimpleUploadedFile from the BytesIO object
    test_image = SimpleUploadedFile(
        name="image.jpg",
        content=image_file.getvalue(),
        content_type="image/jpeg"
    )
    return test_image


def test_create_image_return_success() -> None:

    """
    Test creating an Image instance.
    """

    test_image_title = "Test Image Title"
    test_image_file = sample_test_image_file()

    test_image = Image.objects.create(
        title=test_image_title,
        image=test_image_file
    )

    # Check if the image was saved correctly
    test_image_counts = Image.objects.count()
    assert test_image_counts == 1

    get_image = Image.objects.get(pk=test_image.pk)
    assert get_image.title == test_image_title
    assert get_image.image
    assert get_image.width == test_image.width
    assert get_image.height == test_image.height
    assert get_image.file_hash
    assert get_image.file_size is not None
    assert get_image.file_size > 0


def test_update_image_return_success(first_test_image: 'Image') -> None:

    """
    Test updating an existing image.

    This test updates the title of an existing image and asserts
    that the changes are successfully saved to the database.

    :param first_test_image: The initial image object created for the test.
    :return: None
    """

    test_image_title = 'image title edited'
    first_test_image.title = test_image_title
    first_test_image.save()
    first_test_image.full_clean()

    get_test_image = Image.objects.get(pk=first_test_image.pk)
    assert get_test_image.title == test_image_title
    assert get_test_image.image == first_test_image.image


def test_create_image_with_duplicate_existence_content_return_error() -> None:

    """
    Test handling duplicate images.

    This test case ensures that attempting to create an image with duplicate content
    raises a DuplicateImageException.
    """

    duplicate_test_image_file = sample_test_image_file()

    Image.objects.create(
        title='first test title', image=duplicate_test_image_file
    )

    second_test_with_duplicate_image = Image.objects.create(
        title='first test title', image=duplicate_test_image_file
    )

    with pytest.raises(DuplicateImageException):
        second_test_with_duplicate_image.full_clean()
