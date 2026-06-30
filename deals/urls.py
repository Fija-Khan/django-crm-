from django.urls import path
from . import views

urlpatterns = [

    path("", views.deal_list, name="deal_list"),

    path("add/", views.deal_create, name="deal_create"),

    path("<int:pk>/", views.deal_detail, name="deal_detail"),

    path("<int:pk>/edit/", views.deal_edit, name="deal_edit"),

    path("<int:pk>/delete/", views.deal_delete, name="deal_delete"),

]