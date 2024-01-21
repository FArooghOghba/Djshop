from rest_framework import serializers

from src.djshop.catalog.models import Category


class CategoryOutPutModelSerializer(
    serializers.ModelSerializer['Category']
):

    """
    Serializer class for converting Category model instances to JSON.

    Meta:
        A nested class containing metadata for the serializer.

    Fields:
        id (int): The unique identifier of the category.
        title (str): The title of the category.
        description (str): An optional description for the category.
        is_public (bool): Indicates whether the category is public or not.
    """

    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'is_public')
