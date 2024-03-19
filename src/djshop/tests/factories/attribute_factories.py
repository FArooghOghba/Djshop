import factory
from factory.django import DjangoModelFactory

from src.djshop.catalog.models import Attribute
from src.djshop.utils.tests.base import faker


class AttributeFactory(DjangoModelFactory):

    """
    Factory for creating instances of the Attribute model.
    """

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))

    class Meta:
        model = Attribute
