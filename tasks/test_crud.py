import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from tasks.models import Tag, Task


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
        pass

    # READ TEST
    def test_get_task_list(self):
        """Test: obtener lista de tareas del usuario"""
        pass

    def test_get_task_detail(self):
        """Test: obtener detalles de una tarea especifica"""

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
        pass

    def test_patch_other_user_task_forbidden(self):
        """Test: no puede  hacer path a tarea de otro usuario"""
        pass

    # DELETE TEST
    def test_delete_other_user_task_forbidden(self):
        """Test: eliminar tarea exitosamente"""
        pass
