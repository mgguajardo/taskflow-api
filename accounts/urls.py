from django.urls import path

from rest_framework.authtoken.views import ObtainAuthToken

from drf_spectacular.utils import extend_schema

from . import views


class SpectacularObtainAuthToken(ObtainAuthToken):
    @extend_schema(
        summary="Obtener token de autenticacion",
        description="Obtiene token de autenticacion usando username y password",
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", SpectacularObtainAuthToken.as_view(), name="login"),
]
