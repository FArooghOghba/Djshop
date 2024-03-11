import django_stubs_ext
from django.contrib import admin

from src.djshop.media.models import Image


django_stubs_ext.monkeypatch()


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin['Image']):

    """
    Admin configuration for the Image model.

    This class defines the behavior of the Image model in
    the Django admin interface.
    """

    # Define the list of fields to be displayed in the admin list view
    list_display = (
        'title',
        'width',
        'height',
        'file_hash',
        'file_size',
    )

    # Enable search functionality based on the title field
    search_fields = ['title__istartswith']
