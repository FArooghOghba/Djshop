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


class OptionGroup(BaseModel):

    """
    option group for making options for a product class.
    """

    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "Option Group"
        verbose_name_plural = "Option Groups"

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
        Returns a human-readable string representation of the option group.

        :returns: str: The title of the option group.
        """

        return self.title


class OptionGroupValues(BaseModel):

    """
    option group values for making values for a product class options.
    """

    title = models.CharField(max_length=255, db_index=True)
    option_group = models.ForeignKey(
        to=OptionGroup, on_delete=models.CASCADE, related_name='values'
    )

    class Meta:
        verbose_name = "Option Group value"
        verbose_name_plural = "Option Group values"

    def __str__(self) -> str:

        """
        Returns a human-readable string representation of the option group.

        :returns: str: The title of the option group.
        """

        return self.title


class Option(BaseModel):

    """
    product attribute for creating attributes for the product.
    """

    class OptionTypeChoice(models.TextChoices):

        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    type = models.CharField(
        max_length=16, choices=OptionTypeChoice.choices,
        default=OptionTypeChoice.text
    )
    group = models.ForeignKey(
        to=OptionGroup, on_delete=models.PROTECT, null=True, blank=True
    )
    required = models.BooleanField(default=False)

    class Meta:
        verbose_name = "option"
        verbose_name_plural = "options"

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
        Returns a human-readable string representation of the product.

        :returns: str: The title of the product.
        """

        return self.title


class ProductClass(BaseModel):

    """
    product class for creating a specific product.
    """

    title = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    track_stock = models.BooleanField(default=True)
    require_shipping = models.BooleanField(default=True)
    option = models.ManyToManyField(to=Option, blank=True)

    class Meta:
        verbose_name = "Product Class"
        verbose_name_plural = "Product Classes"

    def has_attributes(self) -> bool:
        return self.attributes.exists()

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
        Returns a human-readable string representation of the product.

        :returns: str: The title of the product.
        """

        return self.title


class Attribute(BaseModel):

    """
    product attribute for creating attributes for the product.
    """

    class AttributeTypeChoice(models.TextChoices):

        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    product_class = models.ForeignKey(
        to=ProductClass, on_delete=models.CASCADE,
        null=True, related_name='attributes'
    )
    title = models.CharField(max_length=255, db_index=True)
    type = models.CharField(
        max_length=16, choices=AttributeTypeChoice.choices,
        default=AttributeTypeChoice.text
    )
    option_group = models.ForeignKey(
        to=OptionGroup, on_delete=models.PROTECT,
        null=True, blank=True, related_name='attributes'
    )
    required = models.BooleanField(default=False)

    class Meta:
        verbose_name = "attribute"
        verbose_name_plural = "attributes"

    def __str__(self) -> str:

        """
        Returns a human-readable string representation of the product.

        :returns: str: The title of the product.
        """

        return self.title
