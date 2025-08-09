from django.shortcuts import render
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Tag
from .serializers import TaskSerializer, TagSerializer
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated


# Vista para listar y crear tareas
class TaskListCreateView(generics.ListCreateAPIView):
    """
    vista para listar todas las tareas (GET) y crear una nueva tarea (POST).
    """

    serializer_class = TaskSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    # Filtra por tareas completadas o por etiqueatas (por id)
    filterset_fields = ["completed", "tags"]
    # Permitir ordenar por etiqueta
    ordering_fields = ["created_at", "title", "tags__name"]
    # Permitir buscar por nombre de etiqueta
    search_fields = ["title", "description", "tags__name"]

    def get_queryset(self):
        # Solo devolver tareas del usuario autenticado, ordenadas por fecha
        return Task.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # Asociar automaticatemente el usuario a la tarea
        serializer.save(user=self.request.user)


# Vista para ver, actualizar o eliminar una tarea individual
class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Restinge el acceso a las tareas del usuario autenticado
        return Task.objects.filter(user=self.request.user)


# Vista para listar y crear etiquetas
class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# Vista para ver, actualizar o eliminar una etiqueta individual
class TagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
