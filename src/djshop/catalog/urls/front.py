from django.urls import path

from src.djshop.catalog.apis.front.category import (
    CategoryNodeAPIView, CategoryTreeAPIView,
)


urlpatterns = [
      path(
            route='categories/',
            view=CategoryTreeAPIView.as_view(),
            name='front-category-list'
      ),

      path(
            route='category/<slug:category_slug>/',
            view=CategoryNodeAPIView.as_view(),
            name='front-category-node'
      )
]
