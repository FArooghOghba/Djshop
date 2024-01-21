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
