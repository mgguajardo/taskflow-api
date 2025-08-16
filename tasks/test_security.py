from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

import pytest

from tasks.models import Task


@pytest.mark.django_db
class TestTaskSecurity:
    """
    Test de seguridad para verificar que los usuarios solo
    puedan acceder a sus propias tareas.
    """

    def setup_method(self):
        """
        Tests de seguridad para verificar que los usuruarios solo
        puedan accder a sus proprias tareas.
        """
        # crer dos usuarios de prueba
        self.user1 = User.objects.create_user(
            username="usuario1",
            password="password123",
        )
        self.user2 = User.objects.create_user(
            username="usuario2", password="password123"
        )

        # crear cliente API
        self.client = APIClient()

        # crear una tarea para user1
        self.task_user1 = Task.objects.create(
            title="Tarea de Usuario 1",
            description="Esta tarea pertenece al usuario 1",
            user=self.user1,
        )

    def test_user_cannot_access_other_user_task(self):
        """
        Test: un usuario no puede a acceder a la tarea de otro usuario
        Debe retortar 404 (no encontrado) para mantener  privacidad
        """
        # Login como usuario2
        self.client.force_authenticate(user=self.user2)

        # intenta acceder a la tarea del usuario1
        url = f"/api/tasks/{self.task_user1.id}/"
        response = self.client.get(url)

        # Verificar que no pudo acceder
        assert response.status_code == status.HTTP_404_NOT_FOUND
