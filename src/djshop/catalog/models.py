from typing import Any, Optional

from django.db import models
from django.utils.text import slugify
from treebeard.mp_tree import MP_Node

from src.djshop.catalog.managers import CategoryQuerySet
from src.djshop.common.models import BaseModel
from src.djshop.utils.db.fields import UpperCaseCharField


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

    @property
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


class Product(BaseModel):

    """
    product for creating a specific product.
    """

    class ProductTypeChoice(models.TextChoices):

        standalone = 'standalone'
        parent = 'parent'
        child = 'child'

    structure = models.CharField(
        max_length=16, choices=ProductTypeChoice.choices,
        default=ProductTypeChoice.standalone
    )
    parent = models.ForeignKey(
        to='self', on_delete=models.CASCADE, related_name='children',
        null=True, blank=True
    )
    product_class = models.ForeignKey(
        to=ProductClass, on_delete=models.PROTECT, related_name='products',
        null=True, blank=True
    )
    title = models.CharField(max_length=128, unique=True, db_index=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    upc = UpperCaseCharField(max_length=24, unique=True, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    meta_title = models.CharField(
        max_length=128, unique=True, db_index=True, null=True, blank=True
    )
    meta_description = models.TextField(null=True, blank=True)
    attributes = models.ManyToManyField(
        to=Attribute, through='catalog.AttributeValue'
    )
    recommendations = models.ManyToManyField(
        to='catalog.Product', through='catalog.Recommendations', blank=True
    )
    categories = models.ManyToManyField(
        to=Category, related_name='categories'
    )

    @property
    def main_image(self) -> Optional["Image"]:

        """
        Retrieve the main image associated with the product.

        :return: Optional[Image]: The main image associated with the product.
        """

        if self.images.exists():
            return self.images.first()
        else:
            return None

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

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


class AttributeValue(BaseModel):

    """
    Represents the value of an attribute for a product.
    """

    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(to=Attribute, on_delete=models.CASCADE)
    value_text = models.TextField(null=True, blank=True)
    value_integer = models.IntegerField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_option = models.ForeignKey(
        to=OptionGroupValues, on_delete=models.PROTECT, null=True, blank=True
    )
    value_multi_option = models.ManyToManyField(
        to=OptionGroupValues, related_name='multi_valued_attribute_value',
        blank=True
    )

    class Meta:
        unique_together = ('product', 'attribute')
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"

    def __str__(self) -> str:

        """
        Returns a human-readable string representation of the attribute value.

        :returns: str: The title of the attribute value.
        """

        return f'{self.product} >> {self.attribute}'


class Recommendations(BaseModel):

    """
    Represents recommendations between products.
    """

    primary = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name='primary'
    )
    normal = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name='normal'
    )
    rank = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('primary', 'normal')
        ordering = ('primary', '-rank')

    def __str__(self) -> str:

        """
        Returns a human-readable string representation of the recommendations.

        :returns: str: The title of the recommendations.
        """

        return f'{self.primary.title} >> {self.rank}'


class Image(BaseModel):

    """
    Represents an image associated with a product.
    """

    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ForeignKey(
        to='media.image', on_delete=models.PROTECT, related_name='products'
    )
    display_order = models.PositiveIntegerField(default=0)

    def delete(self, *args: Any, **kwargs: Any) -> Any:

        """
        Delete the image instance.

        Overrides the delete method to update the display order of
        remaining images associated with the product after deletion.
        """

        super().delete(*args, **kwargs)

        images = self.product.images.all()
        for index, image in enumerate(iterable=images):
            image.display_order = index
            image.save()

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ('display_order',)
