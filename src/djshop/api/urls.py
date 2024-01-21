from django.urls import include, path


app_name = 'api'


urlpatterns = [
      path(
            route='catalog/',
            view=include(('src.djshop.catalog.urls.front', 'catalog'))
      )
]
