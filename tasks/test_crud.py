import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from tasks.models import Task


@pytest.mark.django_db
class TestTaskCRUD:
    """
    Suite completa de test para operaciones CRUD de tareas,
    Cubre: Create, Read, Updaate (PUT/PATCH), Delete
    """

    def setup_method(self):
        """Configuracion que se ejecuta antes de cada test"""
        # Crear usuario de pruebas
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpass123"
        )
        # Cliente API
        self.client = APIClient()

        # Tarea base para test de Uptade/Delete
        self.task = Task.objects.create(
            title="Tarea de prueba",
            description="Descripcion original",
            completed=False,
            user=self.user1,
        )

    # CREATE TEST
    def test_create_task_succes(self):
        """Test: crear tarea exitosamente"""
        # RED: Escribimos el test antes de que le funcionalidad exista

        # Autenticar usuario
        self.client.force_authenticate(user=self.user1)

        # Datos para crear nueva tarea
        task_data = {
            "title": "Nueva tarea desde API",
            "description": "Descripcion de la nueva tarea",
            "completed": False,
        }

        # Ejecutar POST
        url = "/api/tasks/"
        response = self.client.post(url, task_data)

        # Verificaciones
        assert response.status_code == status.HTTP_201_CREATED

        # Verificar que la tarea se creo en DB
        assert Task.objects.filter(title="Nueva tarea desde API").exists()

        # Verificar que pertenece al usuario correcto
        created_task = Task.objects.get(title="Nueva tarea desde API")
        assert created_task.user == self.user1
        assert created_task.description == "Descripcion de la nueva tarea"
        assert not created_task.completed

    def test_get_task_detail(self):
        """Test: obtener detalles de una tarea especifica"""
        # Autenticar usuarios propietarios
        self.client.force_authenticate(user=self.user1)

        # Ejecutar GET a detalle de tarea
        url = f"/api/tasks/{self.task.id}/"
        response = self.client.get(url)

        # Verificar respuesta exitosa
        assert response.status_code == status.HTTP_200_OK

        # Verificar datos en response
        response_data = response.json()
        assert response_data["id"] == self.task.id
        assert response_data["title"] == "Tarea de prueba"
        assert response_data["description"] == "Descripcion original"
        assert not response_data["completed"]

    # UPDATE TEST (aqui va nuestro PATCH tests)
    def test_patch_task_title_only(self):
        """Test: actualizar solo el titulo usando patch"""
        # Autenticar usuario propietario
        self.client.force_authenticate(user=self.user1)

        # Preparar datos para PATCH (solo titulo)
        url = f"/api/tasks/{self.task.id}/"
        patch_data = {"title": "Titulo actualizado con PATCH"}
        # Ejecutar PATCH (solo titulo)
        response = self.client.patch(url, patch_data)
        # Verificar respuestas
        assert response.status_code == status.HTTP_200_OK

        # Verificar que solo cambio el titulo
        self.task.refresh_from_db()
        assert self.task.title == "Titulo actualizado con PATCH"
        assert self.task.description == "Descripcion original"
        assert not self.task.completed

    def test_patch_task_multiple_fields(self):
        """Test: actualizando multiples campos usando PATCH"""
        # Autenticar usuario propietario
        self.client.force_authenticate(user=self.user1)

        # Preparar datos para PATC (multiples campos)
        url = f"/api/tasks/{self.task.id}/"
        patch_data = {
            "title": "Titulo actualizado multiple",
            "description": "Nueva descripcion actualizada",
            "completed": True,
        }

        # Ejecutar PATC
        response = self.client.patch(url, patch_data)

        # Verificar respuesta existosa
        assert response.status_code == status.HTTP_200_OK

        # Verificar que TODOS los campos cambiaron
        self.task.refresh_from_db()
        assert self.task.title == "Titulo actualizado multiple"
        assert self.task.description == "Nueva descripcion actualizada"
        assert self.task.completed
        assert self.task.user == self.user1
