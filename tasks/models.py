from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Tag(models.Model):
    """
    Representa una etiqueta o categoria que se puede asignar a una tarea.
    Ejemplos: "trabajo", "Personal", "Urgente".
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """
        Devuelve una representacion en string del objeto, que por convención
        en Django es el campo mas descriptivo. Se usa en el admin de Django
        """
        return self.name


class Task(models.Model):
    """
    Representa una tarea especifica en la lista de quehaceres.
    Cada tarea esta asociada a un usuario y puede tener multiples etiquetas.
    """

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relaciones
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        """
        Representación en string de la tarea, util para la depuracion y el admin.
        """
        return self.title
