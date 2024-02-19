import factory
from factory.django import DjangoModelFactory

from src.djshop.catalog.models import Option, OptionGroup, ProductClass
from src.djshop.utils.tests.base import faker


class OptionGroupFactory(DjangoModelFactory):

    """
    Factory for creating instances of the OptionGroup model.
    """

    class Meta:
        model = OptionGroup

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))


class OptionFactory(DjangoModelFactory):

    """
    Factory for creating instances of the Option model.
    """

    class Meta:
        model = Option

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))


class ProductClassFactory(DjangoModelFactory):

    """
    Factory for creating instances of the Product Class model.
    """

    class Meta:
        model = ProductClass

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))
    description = factory.LazyAttribute(lambda x: faker.text())
