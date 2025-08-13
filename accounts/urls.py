from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
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
