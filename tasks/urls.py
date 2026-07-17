from django.urls import path

from .views import (
    task_list,
    TaskCreateView,
    TaskUpdateView,
    task_complete,
    task_detail,
    task_delete,
)

app_name = "tasks"

urlpatterns = [
    path("", task_list, name="task_list"),
    path("add/", TaskCreateView.as_view(), name="task_add"),
    path("<int:pk>/", task_detail, name="task_detail"),
    path("<int:pk>/edit/", TaskUpdateView.as_view(), name="task_edit"),
    path("<int:pk>/complete/", task_complete, name="task_complete"),
    path("<int:pk>/delete/", task_delete, name="task_delete"),
]