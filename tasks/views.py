from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from .models import Tag, Task
from .permissions import IsOwner
from .serializers import TagSerializer, TaskSerializer


# Vista para listar y crear tareas
class TaskListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar todas las tareas (GET) y crear una nueva tarea (POST).
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    # Filtrar por tareas completadas o por etiquetas (por id)
    filterset_fields = ["completed", "tags"]
    # Permitir ordenar por fecha de creación, título o nombre de etiqueta
    ordering_fields = ["created_at", "title", "tags__name"]
    # Permitir buscar por título, descripción o nombre de etiqueta
    search_fields = ["title", "description", "tags__name"]

    def get_queryset(self):
        # Para spectacular: evitar error cuando no hay usuario autenticado
        if getattr(self, "swagger_fake_view", False):
            return Task.objects.none()
        return Task.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # Asociar automáticamente el usuario a la tarea
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Listar tareas del usuario",
        description="Obtiene todas las tareas del usuario autenticado con opciones de filtrado, búsqueda y ordenamiento",
        tags=["Tasks"],
        parameters=[
            OpenApiParameter(
                name="completed",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filtrar por estado completado (true/false)",
            ),
            OpenApiParameter(
                name="tags",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filtrar por ID de etiqueta",
            ),
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Buscar en título, descripción o nombre de etiqueta",
            ),
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Ordenar por: created_at, title, tags__name (usar - para orden descendente)",
            ),
        ],
        responses={
            200: TaskSerializer(many=True),
            401: {"description": "No autenticado"},
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Crear nueva tarea",
        description="Crea una nueva tarea para el usuario autenticado. El título debe ser único por usuario.",
        tags=["Tasks"],
        request=TaskSerializer,
        responses={
            201: TaskSerializer,
            400: {
                "description": "Error de validación - datos inválidos o título duplicado"
            },
            401: {"description": "No autenticado"},
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# Vista para ver, actualizar o eliminar una tarea individual
class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Para spectacular: evitar error cuando no hay usuario autenticado
        if getattr(self, "swagger_fake_view", False):
            return Task.objects.none()
        # Restringe el acceso a las tareas del usuario autenticado
        return Task.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Obtener tarea específica",
        description="Obtiene los detalles de una tarea específica del usuario autenticado",
        tags=["Tasks"],
        responses={
            200: TaskSerializer,
            401: {"description": "No autenticado"},
            403: {"description": "No tienes permisos para acceder a esta tarea"},
            404: {"description": "Tarea no encontrada"},
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar tarea completa",
        description="Actualiza todos los campos de una tarea específica del usuario",
        tags=["Tasks"],
        request=TaskSerializer,
        responses={
            200: TaskSerializer,
            400: {"description": "Error de validación"},
            401: {"description": "No autenticado"},
            403: {"description": "No tienes permisos para modificar esta tarea"},
            404: {"description": "Tarea no encontrada"},
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Actualización parcial de tarea",
        description="Actualiza parcialmente los campos de una tarea específica del usuario",
        tags=["Tasks"],
        request=TaskSerializer,
        responses={
            200: TaskSerializer,
            400: {"description": "Error de validación"},
            401: {"description": "No autenticado"},
            403: {"description": "No tienes permisos para modificar esta tarea"},
            404: {"description": "Tarea no encontrada"},
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar tarea",
        description="Elimina permanentemente una tarea específica del usuario",
        tags=["Tasks"],
        responses={
            204: {"description": "Tarea eliminada exitosamente"},
            401: {"description": "No autenticado"},
            403: {"description": "No tienes permisos para eliminar esta tarea"},
            404: {"description": "Tarea no encontrada"},
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# Vista para listar y crear etiquetas
class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Listar todas las etiquetas",
        description="Obtiene la lista completa de etiquetas disponibles en el sistema",
        tags=["Tags"],
        responses={
            200: TagSerializer(many=True),
            401: {"description": "No autenticado"},
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Crear nueva etiqueta",
        description="Crea una nueva etiqueta en el sistema",
        tags=["Tags"],
        request=TagSerializer,
        responses={
            201: TagSerializer,
            400: {"description": "Error de validación - nombre duplicado o inválido"},
            401: {"description": "No autenticado"},
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# Vista para ver, actualizar o eliminar una etiqueta individual
class TagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Obtener etiqueta específica",
        description="Obtiene los detalles de una etiqueta específica por su ID",
        tags=["Tags"],
        responses={
            200: TagSerializer,
            401: {"description": "No autenticado"},
            404: {"description": "Etiqueta no encontrada"},
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Actualizar etiqueta completa",
        description="Actualiza todos los campos de una etiqueta específica",
        tags=["Tags"],
        request=TagSerializer,
        responses={
            200: TagSerializer,
            400: {"description": "Error de validación"},
            401: {"description": "No autenticado"},
            404: {"description": "Etiqueta no encontrada"},
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Actualización parcial de etiqueta",
        description="Actualiza parcialmente los campos de una etiqueta específica",
        tags=["Tags"],
        request=TagSerializer,
        responses={
            200: TagSerializer,
            400: {"description": "Error de validación"},
            401: {"description": "No autenticado"},
            404: {"description": "Etiqueta no encontrada"},
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Eliminar etiqueta",
        description="Elimina permanentemente una etiqueta específica del sistema",
        tags=["Tags"],
        responses={
            204: {"description": "Etiqueta eliminada exitosamente"},
            401: {"description": "No autenticado"},
            404: {"description": "Etiqueta no encontrada"},
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
