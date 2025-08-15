import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from tasks.models import Tag, Task


@pytest.mark.django_db
class TestTaskFiltering:
    """
    Tests para verificar que el filtrado de tareas funciona
    """

    def setup_method(self):
        """Configuración que se ejecuta antes de cada test"""
        # Crear usuarios
        self.user1 = User.objects.create_user(
            username="usuario1",
            password="password123",
        )
        self.user2 = User.objects.create_user(
            username="usuario2",
            password="password123",
        )

        # Crear cliente API
        self.client = APIClient()

        # Crear etiquetas (globales - sin campo user)
        self.tag_trabajo = Tag.objects.create(name="trabajo")
        self.tag_personal = Tag.objects.create(name="personal")

        # Crear tareas para user1
        self.task1_trabajo = Task.objects.create(
            title="reunion importante",
            description="reunion con cliente",
            user=self.user1,
        )
        self.task1_trabajo.tags.add(self.tag_trabajo)

        self.task1_personal = Task.objects.create(
            title="comprar viveres",
            description="lista del supermercado",
            user=self.user1,
        )
        self.task1_personal.tags.add(self.tag_personal)

        # Crear tarea para user2
        self.task2_trabajo = Task.objects.create(
            title="revisar codigo",
            description="code review",
            user=self.user2,
        )
        self.task2_trabajo.tags.add(self.tag_trabajo)

    def test_filter_task_by_tag(self):
        """
        Test: Filtrar tareas por etiqueta devuelve solo las tareas correctas
        """
        # Login como usuario1
        self.client.force_authenticate(user=self.user1)

        # Filtrar por etiqueta 'trabajo'
        url = f"/api/tasks/?tags={self.tag_trabajo.id}"
        response = self.client.get(url)

        # Verificaciones
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == "reunion importante"

    def test_filter_by_completed_status(self):
        """
        Test: Filtrar por estado completado funciona
        """
        # Marcar una tarea como completada
        self.task1_trabajo.completed = True
        self.task1_trabajo.save()

        # Login como usuario1
        self.client.force_authenticate(user=self.user1)

        # Filtrar por tareas completadas
        url = "/api/tasks/?completed=true"
        response = self.client.get(url)

        # Verificaciones
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["completed"] is True

    def test_unique_title_per_user_creation(self):
        """
        Test: No se puede crear una tarea con titulo duplicado para el mismo usuario
        """
        # Login como usuario1
        self.client.force_authenticate(user=self.user1)

        # Interar crear una tardea con titulo que ya existe para user1
        data = {
            "title": "reunion importante",
            "description": "Otra reunion",
        }

        response = self.client.post("/api/tasks/", data)

        # Debe retornar error 400(bad request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "ya existe una tarea con este titulo" in str(response.data).lower()

    def test_different_users_can_have_same_title(self):
        """
        Test: Usuarios diferentes si pueden crear tareas con el mismo titulo
        """
        # Login como usuario2
        self.client.force_authenticate(user=self.user2)
        # crear tarea con titulo qur ya existe para user1
        data = {
            "title": "reunion importante",
            "description": "mi reunion",
        }
        response = self.client.post("/api/tasks/", data)

        # Debe permitir la edicion (200 OK)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "reunion importante"
        assert response.data["description"] == "mi reunion"

    def test_edit_to_existing_title_not_allowed(self):
        """
        Test: Al editar, no se puede cambiar a un titulo
        que ya existe para el mismo usuario
        """
        self.client.force_authenticate(user=self.user1)

        # Intentar cambiar task1_trabajo al titulo de task1_personal
        data = {
            "title": "comprar viveres",
            "description": "nueva descripcion",
        }

        url = f"/api/tasks/{self.task1_trabajo.id}/"
        response = self.client.put(url, data)

        # Debe retornar error 400
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "ya existe una tarea con este titulo" in str(response.data).lower()
