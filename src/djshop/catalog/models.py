from typing import Any

from django.db import models
from django.utils.text import slugify
from treebeard.mp_tree import MP_Node

from src.djshop.catalog.managers import CategoryQuerySet
from src.djshop.common.models import BaseModel


class Category(MP_Node, BaseModel):

    """
    Model representing a hierarchical category structure using Django
    Treebeard's MP_Node.
    Inherits from BaseModel for common fields like created_at, updated_at.

    Attributes:
        title (str): The title of the category.
        slug (str): The slugified version of the title used for URLs.
        description (str): An optional description for the category.
        is_public (bool): Indicates whether the category is public or not.
    """

    title = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    is_public = models.BooleanField(default=True)

    objects = CategoryQuerySet.as_manager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args: Any, **kwargs: Any) -> None:

        """
        Overrides the save method to generate the slug based on the title.

        :param: args: Variable length argument list.
        :param: kwargs: Arbitrary keyword arguments.
        """

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:

        """
        Returns a human-readable string representation of the category.

        :returns: str: The title of the category.
        """

        return self.title
