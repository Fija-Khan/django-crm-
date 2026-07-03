from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Note
from .forms import NoteForm


# -----------------------------
# NOTE LIST
# -----------------------------
class NoteListView(LoginRequiredMixin, ListView):

    model = Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Note.objects.select_related(
                "contact",
                "lead",
                "created_by"
            )

        return Note.objects.filter(
            created_by=self.request.user
        ).select_related(
            "contact",
            "lead"
        )


# -----------------------------
# ADD NOTE
# -----------------------------
class NoteCreateView(LoginRequiredMixin, CreateView):

    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("note_list")

    def form_valid(self, form):

        form.instance.created_by = self.request.user

        return super().form_valid(form)


# -----------------------------
# EDIT NOTE
# -----------------------------
class NoteUpdateView(LoginRequiredMixin, UpdateView):

    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_url = reverse_lazy("note_list")

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Note.objects.all()

        return Note.objects.filter(
            created_by=self.request.user
        )


# -----------------------------
# DELETE NOTE
# -----------------------------
class NoteDeleteView(LoginRequiredMixin, DeleteView):

    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("note_list")

    def get_queryset(self):

        if self.request.user.role == "admin":
            return Note.objects.all()

        return Note.objects.filter(
            created_by=self.request.user
        )