from typing import Any, Dict, Type

import factory
from factory.django import DjangoModelFactory

from src.djshop.catalog.models import Category
from src.djshop.utils.tests.base import faker


class CategoryFactory(DjangoModelFactory):

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

    @classmethod
    def create_payload(cls) -> Dict[str, 'factory.LazyAttribute']:

        """
        A class method that generates a payload dictionary for creating
        a category via the API.

        :return: generate a payload dictionary with consistent values
        for creating category via the API.
        """

        test_category = cls.build()
        return {
            'title': test_category.title,
            'description': test_category.description,
        }
