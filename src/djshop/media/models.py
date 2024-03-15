import hashlib
import os
import uuid
from typing import Any

from django.db import models

from src.djshop.common.models import BaseModel
from src.djshop.core.exceptions import DuplicateImageException


def image_file_path(instance: Any, filename: str) -> str:

    """
    Generate a file path for a new image.

    This function generates a file path for a new image based
    on the provided filename.
    It uses a UUID to ensure uniqueness and appends it to the
    'uploads/images' directory.

    :param filename: The original filename of the image.
    :param instance: The original filename of the image.
    :return: str: The generated file path.
    """

    extension = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{extension}'

    return os.path.join('uploads', 'images', filename)


class Image(BaseModel):

    """
    Model representing an image.

    This model stores information about an image, including
    its title, dimensions, file hash, file size, and focal point coordinates.
    """

    title = models.CharField(max_length=128)
    image = models.ImageField(
        width_field='width', height_field='height',
        upload_to=image_file_path
    )

    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)

    file_hash = models.CharField(max_length=40, db_index=True, editable=False)
    file_size = models.PositiveIntegerField(null=True, editable=False)

    focal_point_x = models.PositiveIntegerField(null=True, blank=True)
    focal_point_y = models.PositiveIntegerField(null=True, blank=True)
    focal_point_width = models.PositiveIntegerField(null=True, blank=True)
    focal_point_height = models.PositiveIntegerField(null=True, blank=True)

    def calculate_hash_and_size_for_file(self) -> None:

        """
        Calculate the hash and size of the image file.

        This method calculates the SHA-1 hash and size of the image file
        and stores them in the corresponding fields of the Image instance.
        """

        if not self.image.closed:

            self.file_size = self.image.size

            hasher = hashlib.sha1()
            for chunk in self.image.file.chunks():
                hasher.update(chunk)

            self.file_hash = hasher.hexdigest()

    def is_duplicate(self) -> bool:

        """
        Check if the image is a duplicate.

        This method calculates the hash and size of the image file
        and checks if any other image in the database has the same hash,
        excluding the current instance if it has been saved to the database.

        :return: bool: True if a duplicate image is found, False otherwise.
        """

        self.calculate_hash_and_size_for_file()

        queryset = Image.objects.filter(file_hash=self.file_hash)
        if self.pk is not None:
            queryset = queryset.exclude(pk=self.pk)
        return queryset.exists()

    def clean(self) -> None:

        """
        Validate the image.

        This method overrides the clean() method to perform additional validation
        before saving the image instance. It checks if the image is a duplicate
        and raises an exception if it is.

        :raises DuplicateImageException: If the image is a duplicate.
        """

        super().clean()

        if self.is_duplicate():
            raise DuplicateImageException("Image is already existed.")

    def save(self, *args: Any, **kwargs: Any) -> None:

        """
        Save the image.

        This method overrides the save() method to calculate the hash and size
        of the image file before saving the instance.

        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """

        self.calculate_hash_and_size_for_file()
        super().save(*args, **kwargs)

    def __str__(self) -> str:

        """
        Returns a human-readable string representation of the image.

        :returns: str: The title of the product.
        """

        return self.title
