from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from src.djshop.catalog import models


@admin.register(models.Category)
class CategoryAdmin(TreeAdmin):

    """
    Admin configuration for the Category model.

    This class customizes the appearance and
    behavior of the Category model in the Django admin interface.
    """

    # Use the "movenodeform_factory" to enable tree manipulation in the admin
    form = movenodeform_factory(models.Category)

    # Define the list of fields to be displayed in the admin list view
    list_display = [
        'title',  # Display the title of the category
        'is_public'  # Display the is_public field
    ]

    # Enable search functionality based on the title field
    search_fields = ['title__istartswith']

    # Prepopulate the slug field based on the title field
    prepopulated_fields = {
        'slug': ['title']
    }
