from typing import cast

from django.db.models import QuerySet

from src.djshop.catalog.models import Category


def get_category_tree() -> QuerySet['Category']:

    """
    Retrieve a queryset containing all root categories.

    This function retrieves a queryset containing all Category
    instances that are at the root level (depth=1).

    Returns:
        QuerySet[Category]: A queryset containing all root Category instances.
    """

    # Filter the Category objects to include only those at the root level (depth=1)
    categories = Category.get_root_nodes()

    # Use cast to explicitly specify the type (helpful for type checkers like mypy)
    return cast(QuerySet['Category'], categories)


def get_category_node(*, category_slug: str) -> 'Category':

    """
    Retrieve detailed information about a specific category by its slug.

    This function retrieves the detailed representation of a category
    based on its slug. It includes information such as the category's
    title, description and public.

    :param category_slug: (str): The slug of the category to retrieve.

    :return: Category: The detailed representation of the category.
    """

    get_category_obj = Category.objects.get(slug=category_slug)

    return get_category_obj
