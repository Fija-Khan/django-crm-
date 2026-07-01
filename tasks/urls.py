from django.urls import path

from .views import (
    task_list,
    TaskCreateView,
    TaskUpdateView,
    task_complete,
)

urlpatterns = [

    path("", task_list, name="task_list"),

    path(
        "add/",
        TaskCreateView.as_view(),
        name="task_add"
    ),

    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),

    path(
        "<int:pk>/complete/",
        task_complete,
        name="task_complete"
    ),
]