from django.urls import path

from src.djshop.catalog.apis.admin.category import CategoryNodeAPIView


urlpatterns = [
      path(
            route='category/',
            view=CategoryNodeAPIView.as_view(),
            name='admin-category-node'
      )
]
