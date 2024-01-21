from django.urls import path

from src.djshop.catalog.apis.front.category import CategoryAPIView


app_name = 'catalog'


urlpatterns = [
      path(
            route='category/',
            view=CategoryAPIView.as_view(),
            name='category-list'
      )
]
