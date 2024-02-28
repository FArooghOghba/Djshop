from typing import TYPE_CHECKING, Any, List, Optional, Tuple

import django_stubs_ext
from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from src.djshop.catalog.models import (
    Attribute, Category, Option, OptionGroup, OptionGroupValues, ProductClass,
)


if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest
    from rest_framework.request import Request


django_stubs_ext.monkeypatch()


@admin.register(Category)
class CategoryAdmin(TreeAdmin):

    """
    Admin configuration for the Category model.

    This class customizes the appearance and behavior of the Category model
    in the Django admin interface. It allows users to easily manage the
    category hierarchy and associated properties.

    in the Django admin interface. It allows users to:
        - View a tree structure of categories.
        - Create, edit, and delete categories.
        - Search for categories by their title.
        - Prepopulate the slug field based on the title.
    """

    # Use the "movenodeform_factory" to enable tree manipulation in the admin
    form = movenodeform_factory(Category)

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


class AttributeInline(admin.TabularInline[Attribute, ProductClass]):

    """
    Inline admin class for displaying and managing attributes directly
    on the ProductClass admin page. This allows for efficient editing
    of related attributes within the same context.

    This inline allows users to:
        - View and edit existing attributes associated with a product class.
        - Create new attributes directly on the product class edit page.
        - Use autocomplete to quickly select existing option groups for
        new attributes.
    """

    model = Attribute
    extra = 2
    autocomplete_fields = ['option_group']


class OptionGroupValuesInline(admin.TabularInline[OptionGroupValues, OptionGroup]):

    """
    Inline admin class for displaying and managing OptionGroupValues directly
    on the OptionGroup admin page. This allows for efficient editing of
    related OptionGroupValues within the same context.

    This inline allows users to:
        - View and edit existing values associated with an option group.
        - Create new values directly on the option group edit page.
    """

    model = OptionGroupValues
    extra = 2


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin[OptionGroup]):

    """
    Admin configuration for the OptionGroup model.

    This class allows users to easily manage option groups,
    which are used to categorize options for products.

    This class allows users to:
        - View, edit, and delete option groups.
        - Search for option groups by their title.
        - Prepopulate the slug field based on the title.
        - Manage related option group values through an inline admin.
    """

    search_fields = ['title']
    prepopulated_fields = {
        'slug': ['title']
    }
    inlines = [OptionGroupValuesInline]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin[Option]):

    """
     Admin configuration for the Option model.

    This class allows users to manage options, which represent various
    characteristics (e.g., size, color) that products can have.

    This class allows users to:
        - View, edit, and delete options.
        - Search for options by their title.
        - View the option type and required status in the list view.
        - Prepopulate the slug field based on the title.
    """

    list_display = [
        'title',
        'type',
        'required'
    ]
    search_fields = ['title']
    prepopulated_fields = {
        'slug': ['title']
    }


class AttributesCountFilter(admin.SimpleListFilter):

    """
    Custom filter for ProductClass admin based on the number
    of associated attributes.

    This filter allows you to filter product classes by
    the number of attributes they possess.
    It provides two options: "Less than 5" and "greater than 5".
    """

    title = 'attributes count'
    parameter_name = 'attributes_count'

    def lookups(
            self, request: 'HttpRequest', model_admin: Any
    ) -> List[Tuple[Any, str]]:

        """
        Defines the filter options displayed in the admin interface.
        """

        return [
            ('< 5', 'Less than 5'),
            ('> 5', 'greater than 5'),
        ]

    def queryset(
            self, request: 'HttpRequest', queryset: 'QuerySet[ProductClass]'
    ) -> Optional['QuerySet[ProductClass]']:

        """
        Filters the queryset based on the selected filter option.
        """

        # .annotate(attributes_count=Count(attributes_count))
        if self.value() == '< 5':
            return queryset.filter(attributes_count__lt=5)
        if self.value() == '> 5':
            return queryset.filter(atrributes_count__gt=5)

        # Default return statement
        return queryset


@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin[ProductClass]):

    """
    Admin configuration for the ProductClass model.

    This class provides a comprehensive interface for managing product classes,
    which define the structure and properties of products. Users can view,
    edit, and perform actions on product classes, as well as access-related
    attributes and options.
    """

    list_display = (
        'title',
        'track_stock',
        'require_shipping',
        'has_attributes',
        'attributes_count'
    )
    search_fields = ('title__istartswith', 'description')
    list_filter = ('track_stock', 'require_shipping', AttributesCountFilter)
    autocomplete_fields = ('option',)
    filter_horizontal = ('option',)
    actions = ('enable_track_stock',)
    prepopulated_fields = {
        'slug': ['title']
    }

    # Inlines to display related models directly on the product class admin page
    inlines = [AttributeInline]

    def attributes_count(self, product_class_opj: 'ProductClass') -> int:

        """
        Returns the number of attributes associated with a product class object.
        Used for displaying the attribute count in the admin list view.
        """

        return product_class_opj.attributes.count()

    @admin.action(description='Enable track stock')
    def enable_track_stock(
            self, request: 'Request', queryset: 'QuerySet[ProductClass]'
    ) -> None:

        """Enable track stock for selected product classes."""

        enabled_track_stock = queryset.update(track_stock=True)
        self.message_user(
            request=request,
            message=f'{enabled_track_stock} product track stock successfully enabled'
        )
