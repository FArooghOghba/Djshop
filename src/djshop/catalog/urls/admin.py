from django.urls import path

from src.djshop.catalog.apis.admin.category import (
    CategoryNodeAPIView, CategoryNodeCreateAPIView, CategoryTreeAPIView,
)


urlpatterns = [
      path(
            route='category/<slug:category_slug>/',
            view=CategoryNodeAPIView.as_view(),
            name='admin-category-node'
      ),

      path(
            route='category/',
            view=CategoryNodeCreateAPIView.as_view(),
            name='admin-create-category-node'
      ),

      path(
            route='categories/',
            view=CategoryTreeAPIView.as_view(),
            name='admin-category-tree'
      )
]
