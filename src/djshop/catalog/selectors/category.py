from typing import cast

from django.db.models import QuerySet

from src.djshop.catalog.models import Category


def get_category_list() -> QuerySet['Category']:
    """
    Retrieve a queryset containing all categories.

    :returns: QuerySet[Category]: A queryset containing all Category instances.
    """

    categories = Category.objects.all()

    # Use cast to explicitly specify the type (helpful for type checkers like mypy)
    return cast(QuerySet['Category'], categories)


def get_category_detail(*, category_slug: str) -> 'Category':

    """
    Retrieve detailed information about a specific category by its slug.

    This function retrieves the detailed representation of a categor
    based on its slug. It includes information such as the category's
    title, description and public.

    :param category_slug: (str): The slug of the category to retrieve.

    :return: Category: The detailed representation of the category.
    """

    get_category_obj = Category.objects.get(slug=category_slug)

    return cast('Category', get_category_obj)