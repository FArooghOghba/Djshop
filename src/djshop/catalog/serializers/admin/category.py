from typing import List, Union

from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict
from typing_extensions import Never

from src.djshop.catalog.models import Category


# Define the maximum depth for category recursion
MAX_DEPTH = 5


class CategoryTreeOutPutModelSerializer(
    serializers.ModelSerializer['Category']
):

    """
    Serializer class for converting Category model instances to JSON.

    This serializer is designed to handle hierarchical relationships
    between categories, representing them in a tree-like structure.

    Meta:
        A nested class containing metadata for the serializer.

    Attributes:
        children (SerializerMethodField): A field representing
        the children of a category.

    Fields:
        id (int): The unique identifier of the category.
        title (str): The title of the category.
        description (str): An optional description for the category.
        is_public (bool): Indicates whether the category is public or not.
    """

    # Define a SerializerMethodField for children categories
    children = serializers.SerializerMethodField()

    def get_children(
            self, category_obj: 'Category'
    ) -> Union[ReturnDict[str, Union[str, int]], List[Never]]:

        """
        Retrieve and serialize the children of a given category.

        This method retrieves the children of a category and serializes
        them using the CategoryTreeOutPutModelSerializer.
        It also includes a check for the maximum depth to prevent infinite
        recursion.

        Args:
            category_obj (Category): The category for which to retrieve
            and serialize children.

        Returns:
            list: A list of serialized children categories.
        """

        # Check the depth of the category
        category_obj_depth = category_obj.depth

        if category_obj_depth > MAX_DEPTH:
            return []

        # Retrieve the children of the category
        get_children_obj: QuerySet['Category'] = category_obj.get_children()

        # Serialize the children categories
        children_serializer = CategoryTreeOutPutModelSerializer(
            get_children_obj, many=True
        ).data

        return children_serializer

    class Meta:
        model = Category
        fields = (
            'id', 'title', 'description', 'is_public', 'children'
        )


class CategoryNodeInPutSerializer(
    serializers.Serializer['Category']
):

    """
    Serializer class for handling input data for a Category node.

    This serializer is designed to validate and deserialize input
    data for a Category node.

    Attributes:
        title (CharField): The title of the category.
        description (CharField): An optional description for the category.
        is_public (BooleanField): Indicates whether the category is public or not.
        parent (SlugField): The parent category of the current category.
    """

    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=2048)
    is_public = serializers.BooleanField()
    parent_node = serializers.SlugField(required=False, allow_null=True)
