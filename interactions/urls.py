from django.urls import path

from .views import (
    InteractionListView,
    InteractionCreateView,
    InteractionUpdateView,
    InteractionDeleteView,
)

urlpatterns = [
    # ---------------------------
    # Interaction List
    # ---------------------------
    path(
        "",
        InteractionListView.as_view(),
        name="interaction_list",
    ),

    # ---------------------------
    # Add Interaction
    # ---------------------------
    path(
        "add/",
        InteractionCreateView.as_view(),
        name="interaction_add",
    ),

    # ---------------------------
    # Edit Interaction
    # ---------------------------
    path(
        "<int:pk>/edit/",
        InteractionUpdateView.as_view(),
        name="interaction_edit",
    ),

    # ---------------------------
    # Delete Interaction
    # ---------------------------
    path(
        "<int:pk>/delete/",
        InteractionDeleteView.as_view(),
        name="interaction_delete",
    ),
]