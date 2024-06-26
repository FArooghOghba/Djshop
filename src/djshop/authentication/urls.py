from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)


urlpatterns = [
        path(
            route='jwt/', view=include(
                (
                    [
                        path('login/', TokenObtainPairView.as_view(), name="login"),
                        path('refresh/', TokenRefreshView.as_view(), name="refresh"),
                        path('verify/', TokenVerifyView.as_view(), name="verify"),
                    ]
                )
            ),
            name="jwt"
        ),
]
