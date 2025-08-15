from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import UserRegisterSerializer


# Create your views here.
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []
