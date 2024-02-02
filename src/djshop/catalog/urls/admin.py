from django.urls import path

from src.djshop.catalog.apis.admin.category import (
    CategoryNodeAPIView, CategoryTreeAPIView,
)


urlpatterns = [
      path(
            route='category/<slug:category_slug>/',
            view=CategoryNodeAPIView.as_view(),
            name='admin-category-node'
      ),

      path(
            route='category/',
            view=CategoryNodeAPIView.as_view(),
            name='admin-category-node'
      ),

      path(
            route='categories/',
            view=CategoryTreeAPIView.as_view(),
            name='admin-category-tree'
      )
]
