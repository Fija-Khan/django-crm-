from django.urls import path
from . import views
from django.http import JsonResponse
import json

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path("add/", views.lead_add, name="lead_add"),
    path("<int:pk>/", views.lead_detail, name="lead_detail"),
    path("<int:pk>/edit/", views.lead_edit, name="lead_edit"),
    path("<int:pk>/delete/", views.lead_delete, name="lead_delete"),
    path("kanban/", views.lead_kanban, name="lead_kanban"),
    path("update-stage/", views.update_stage, name="update_stage"),

]