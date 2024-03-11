from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from factory.django import DjangoModelFactory
from PIL import Image as PILImage  # type: ignore

from src.djshop.media.models import Image


def sample_test_image_file(
        width: int = 100, height: int = 100
) -> 'SimpleUploadedFile':

    """
    Generates a test image file.

    This function creates a test image file
    and returns it as a SimpleUploadedFile object.

    :return: SimpleUploadedFile: test image file.
    """

    # Create a BytesIO object to hold the image data
    image_file = BytesIO()

    # Create a new PIL Image with the specified dimensions
    image = PILImage.new(mode='RGB', size=(width, height))

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


class ImageFactory(DjangoModelFactory):

    """
    Factory for creating instances of the Image model.
    """

    image = sample_test_image_file()

    class Meta:
        model = Image
