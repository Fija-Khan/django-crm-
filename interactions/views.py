from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Interaction
from .forms import InteractionForm


# ---------------------------
# INTERACTION LIST
# ---------------------------
class InteractionListView(LoginRequiredMixin, ListView):
    model = Interaction
    template_name = "interactions/interaction_list.html"
    context_object_name = "interactions"
    ordering = ["-interaction_date"]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return Interaction.objects.select_related(
                "contact",
                "lead",
                "logged_by",
            )

        return Interaction.objects.filter(
            logged_by=user
        ).select_related(
            "contact",
            "lead",
            "logged_by",
        )


# ---------------------------
# CREATE INTERACTION
# ---------------------------
class InteractionCreateView(LoginRequiredMixin, CreateView):
    model = Interaction
    form_class = InteractionForm
    template_name = "interactions/interaction_form.html"
    success_url = reverse_lazy("interaction_list")

    def form_valid(self, form):
        form.instance.logged_by = self.request.user
        return super().form_valid(form)


# ---------------------------
# UPDATE INTERACTION
# ---------------------------
class InteractionUpdateView(LoginRequiredMixin, UpdateView):
    model = Interaction
    form_class = InteractionForm
    template_name = "interactions/interaction_form.html"
    success_url = reverse_lazy("interaction_list")

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return Interaction.objects.all()

        return Interaction.objects.filter(logged_by=user)


# ---------------------------
# DELETE INTERACTION
# ---------------------------
class InteractionDeleteView(LoginRequiredMixin, DeleteView):
    model = Interaction
    template_name = "interactions/interaction_confirm_delete.html"
    success_url = reverse_lazy("interaction_list")

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return Interaction.objects.all()

        return Interaction.objects.filter(logged_by=user)