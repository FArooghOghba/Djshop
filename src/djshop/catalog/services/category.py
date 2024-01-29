from typing import Dict, cast

from src.djshop.catalog.models import Category


def create_category_node(*, category_node_data: Dict[str, str]) -> 'Category':

    """
    Create a new Category node.

    This function creates a new Category node with the given data. If a parent_node
    slug is provided, the new node is added as a child of the parent.
    Otherwise, the new node is added as a root node.

    Args:
        category_node_data (Dict[str, str]): The data for the new Category node.
            This should include the fields for the Category model, and optionally
            a 'parent_node' field with the slug of the parent Category.

    Returns:
        Category: The created Category node.
    """

    category_parent_node_slug = category_node_data.pop('parent_node', None)

    if category_parent_node_slug is None:
        category_obj = Category.add_root(**category_node_data)
    else:
        category_parent_node = Category.objects.get(slug=category_parent_node_slug)
        category_obj = cast(
            'Category',
            category_parent_node.add_child(**category_node_data)
        )

    return category_obj
