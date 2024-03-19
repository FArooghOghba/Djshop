from typing import Any, List, Optional

import factory
from factory.django import DjangoModelFactory
from factory.helpers import post_generation

from src.djshop.catalog.models import Attribute, Product
from src.djshop.utils.tests.base import faker


class ProductFactory(DjangoModelFactory):

    """
    Factory for creating instances of the Product model.

    This factory generates Product instances with randomized
    attributes for testing purposes.
    """

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))

    class Meta:
        model = Product

    @post_generation
    def attributes(
            self, create: bool, extracted: Optional[List[Attribute]], **kwargs: Any
    ) -> None:

        """
        Generate random attributes for the created Product instance.

        This method adds random attributes to the created Product instance.
        If the 'create' parameter is False or no attributes are provided,
        no attributes will be added.

        :param create: Boolean flag indicating whether to create attributes.
        :param extracted: Optional list of Attribute instances to add to the Product.
        :param kwargs: Additional keyword arguments.
        """

        if not create:
            return

        if extracted:
            for attribute in extracted:
                self.attributes.add(attribute)
