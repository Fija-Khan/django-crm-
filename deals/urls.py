from django.urls import path
from . import views

app_name = "deals"

urlpatterns = [

    # ==========================
    # DEAL LIST
    # ==========================
    path(
        "",
        views.deal_list,
        name="deal_list",
    ),

    # ==========================
    # CREATE DEAL
    # ==========================
    path(
        "add/",
        views.deal_create,
        name="deal_create",
    ),

    # ==========================
    # DEAL DETAIL
    # ==========================
    path(
        "<int:pk>/",
        views.deal_detail,
        name="deal_detail",
    ),

    # ==========================
    # EDIT DEAL
    # ==========================
    path(
        "<int:pk>/edit/",
        views.deal_edit,
        name="deal_edit",
    ),

    # ==========================
    # DELETE DEAL
    # ==========================
    path(
        "<int:pk>/delete/",
        views.deal_delete,
        name="deal_delete",
    ),

]