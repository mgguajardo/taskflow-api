from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Permiso que solo permite al propietario de la tarea accederla o modificarla
    """

    def has_object_permission(self, request, view, obj):
        # Comprueba si el usuario del objeto es mismo que el usuario autenticado
        return obj.user == request.user
