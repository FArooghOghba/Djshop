from django.urls import path

from src.djshop.catalog.apis.front.category import (
    CategoryDetailAPIView, CategoryListAPIView,
)


urlpatterns = [
      path(
            route='categories/',
            view=CategoryListAPIView.as_view(),
            name='category-list'
      ),

      path(
            route='category/<slug:category_slug>/',
            view=CategoryDetailAPIView.as_view(),
            name='category-detail'
      )
]
