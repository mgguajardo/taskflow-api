from django.urls import path
from .views import UserRegisterView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("auth-token/", obtain_auth_token, name="api-token"),
]
