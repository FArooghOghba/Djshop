from typing import Any, Type

import factory

from src.djshop.catalog.models import Category
from src.djshop.utils.tests.base import faker


class CategoryFactory(factory.django.DjangoModelFactory):

    """
    Factory for creating instances of the Category model.
    """

    class Meta:
        model = Category

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))
    slug = factory.LazyAttribute(lambda _: faker.slug())
    description = factory.LazyAttribute(lambda x: faker.text())

    @classmethod
    def _create(
            cls, model_class: Type[Category] = Category, **kwargs: Any
    ) -> Category:

        """
        Custom _create method to create a Category instance and add it as a root.

        :params: model_class (Type[Category]): The Category model class.
        :params: **kwargs (Any): Additional keyword arguments for creating
                            the instance.

        :returns: Category: The created Category instance.
        """

        instance = model_class(**kwargs)
        return model_class.add_root(instance=instance)
