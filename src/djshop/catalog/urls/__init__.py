from django.urls import include, path


app_name = 'catalog'


urlpatterns = [
      path(
            route='front/',
            view=include(arg='src.djshop.catalog.urls.front')
      ),

      path(
            route='admin/',
            view=include(arg='src.djshop.catalog.urls.admin')
      ),
]
