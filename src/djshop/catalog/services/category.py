from typing import Dict, cast

from src.djshop.catalog.models import Category
from src.djshop.common.services import model_update


def create_category_node(*, category_node_data: Dict[str, str]) -> 'Category':

    """
    Create a new Category node.

    This function creates a new Category node with the given data. If a parent_node
    slug is provided, the new node is added as a child of the parent.
    Otherwise, the new node is added as a root node.

    :param: category_node_data (Dict[str, str]): The data for the new Category node.
            This should include the fields for the Category model, and optionally
            a 'parent_node' field with the slug of the parent Category.

    :returns: Category: The created Category node.
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


def update_category_node(
    *, category_slug: str, category_node_data: Dict[str, str]
) -> 'Category':

    """
    Update a category node in the database based on the provided
    category_slug.

    This function retrieves the category node with the given slug
    from the database, updates the specified fields (title, description,
    is_public) with the provided data, and saves the changes.

    :param category_slug: The unique slug identifying the category node
    to be updated.
    :param category_node_data: A dictionary containing the updated
    data for the category node.
    It may include 'title', 'description', and 'is_public' fields.

    :return: The updated Category node instance.
    """

    # Define the fields that can be updated.
    fields = ['title', 'description', 'is_public']

    # Retrieve the existing category node from the database based on the slug.
    get_category_node = cast(
        'Category',
        Category.objects.get(slug=category_slug)
    )

    # Perform the update using the model_update function.
    updated_category_node, has_updated = model_update(
        instance=get_category_node, fields=fields, data=category_node_data
    )

    return updated_category_node


def delete_category_node(
    *, category_slug: str
) -> None:

    """
    Deletes a category node with the provided category slug.

    This function first retrieves the category object based on the provided
    category_slug and then proceeds to delete the category object.

    :raises Movie.DoesNotExist: If no category with the provided category_slug exists
        in the database.

    :param category_slug: (str): The unique slug identifying the category.

    :return: None
    """

    get_category_node = cast(
        'Category',
        Category.objects.get(slug=category_slug)
    )

    get_category_node.delete()
