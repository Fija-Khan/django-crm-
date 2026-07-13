from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Task
from .forms import TaskForm


# ---------------------------
# TASK LIST
# ---------------------------
@login_required
def task_list(request):

    if request.user.role == "admin":
        tasks = Task.objects.select_related(
            "assigned_to",
            "related_contact",
            "related_lead"
        ).order_by("due_date")

    else:
        tasks = Task.objects.filter(
            assigned_to=request.user
        ).select_related(
            "related_contact",
            "related_lead"
        ).order_by("due_date")

    return render(
        request,
        "tasks/task_list.html",
        {
            "tasks": tasks
        }
    )


# ---------------------------
# CREATE TASK
# ---------------------------
class TaskCreateView(LoginRequiredMixin, CreateView):

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):

        if not form.instance.assigned_to:
            form.instance.assigned_to = self.request.user

        messages.success(
            self.request,
            "Task created successfully."
        )

        return super().form_valid(form)


# ---------------------------
# UPDATE TASK
# ---------------------------
class TaskUpdateView(LoginRequiredMixin, UpdateView):

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):

        user = self.request.user

        if user.role == "admin":
            return Task.objects.all()

        return Task.objects.filter(
            assigned_to=user
        )


    def form_valid(self, form):

        messages.success(
            self.request,
            "Task updated successfully."
        )

        return super().form_valid(form)


# ---------------------------
# MARK TASK COMPLETE
# ---------------------------
@login_required
def task_complete(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    if request.user.role != "admin" and task.assigned_to != request.user:
        return redirect("task_list")

    task.status = "done"
    task.save()

    messages.success(
        request,
        "Task marked as completed."
    )

    return redirect("task_list")


# ---------------------------
# TASK DETAIL
# ---------------------------
@login_required
def task_detail(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    if request.user.role != "admin" and task.assigned_to != request.user:
        return redirect("task_list")

    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task
        }
    )


# ---------------------------
# DELETE TASK
# ---------------------------
@login_required
def task_delete(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk
    )

    if request.user.role != "admin" and task.assigned_to != request.user:
        return redirect("task_list")

    if request.method == "POST":

        task.delete()

        messages.success(
            request,
            "Task deleted successfully."
        )

        return redirect("task_list")

    return render(
        request,
        "tasks/task_confirm_delete.html",
        {
            "task": task
        }
    )