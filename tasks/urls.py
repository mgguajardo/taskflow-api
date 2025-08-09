from django.urls import path
from .views import (
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    TagListCreateView,
    TagRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("tasks/", TaskListCreateView.as_view(), name="task-list"),
    path(
        "tasks/<int:pk>/", TaskRetrieveUpdateDestroyView.as_view(), name="task-detail"
    ),
    path("tags/", TagListCreateView.as_view(), name="tag-list"),
    path("tags/<int:pk>/", TagRetrieveUpdateDestroyView.as_view(), name="tag-detail"),
]
