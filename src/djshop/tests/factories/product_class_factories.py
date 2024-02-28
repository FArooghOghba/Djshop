from typing import Any, List, Optional

import factory
from factory.django import DjangoModelFactory
from factory.helpers import post_generation

from src.djshop.catalog.models import (
    Attribute, Option, OptionGroup, OptionGroupValues, ProductClass,
)
from src.djshop.utils.tests.base import faker


class OptionGroupFactory(DjangoModelFactory):

    """
    Factory for creating instances of the OptionGroup model.
    """

    class Meta:
        model = OptionGroup

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))


class OptionGroupValuesFactory(DjangoModelFactory):

    """
    Factory for creating instances of the OptionGroupValues model.
    """

    class Meta:
        model = OptionGroupValues

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))
    groups = factory.SubFactory(factory=OptionGroupFactory)


class OptionFactory(DjangoModelFactory):

    """
    Factory for creating instances of the Option model.
    """

    class Meta:
        model = Option

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))
    group = factory.SubFactory(factory=OptionGroupFactory)


class ProductClassFactory(DjangoModelFactory):

    """
    Factory for creating instances of the Product Class model.
    """

    class Meta:
        model = ProductClass

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))
    description = factory.LazyAttribute(lambda x: faker.text())

    @post_generation
    def option(
            self, create: bool, extracted: Optional[List[Option]], **kwargs: Any
    ) -> None:

        if not create:
            return

        if extracted:
            for option in extracted:
                self.option.add(option)


class AttributeFactory(DjangoModelFactory):

    """
    Factory for creating instances of the Attribute model.
    """

    class Meta:
        model = Attribute

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))
    option_group = factory.SubFactory(factory=OptionGroupFactory)
    product_class = factory.SubFactory(factory=ProductClassFactory)
