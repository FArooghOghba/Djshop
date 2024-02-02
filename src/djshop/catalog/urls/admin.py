from django.urls import path

from src.djshop.catalog.apis.admin.category import (
    CategoryNodeGetAPIView, CategoryNodePostAPIView, CategoryTreeAPIView,
)


urlpatterns = [
      path(
            route='category/<slug:category_slug>/',
            view=CategoryNodeGetAPIView.as_view(),
            name='admin-get-category-node'
      ),

      path(
            route='category/',
            view=CategoryNodePostAPIView.as_view(),
            name='admin-create-category-node'
      ),

      path(
            route='categories/',
            view=CategoryTreeAPIView.as_view(),
            name='admin-category-tree'
      )
]
