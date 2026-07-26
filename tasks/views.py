from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView

from .forms import TaskForm
from .models import Task


# ==========================================================
# HELPER FUNCTION
# ==========================================================

def get_user_tasks(user):

    tasks = Task.objects.select_related(
        "assigned_to",
        "related_contact",
        "related_lead",
    )

    if user.role == "admin":
        return tasks

    return tasks.filter(
        assigned_to=user
    )


# ==========================================================
# TASK LIST
# ==========================================================

@login_required
def task_list(request):

    tasks = (
        get_user_tasks(request.user)
        .order_by(
            "due_date",
            "-created_at",
        )
    )

    # ----------------------------------
    # Search
    # ----------------------------------

    search = request.GET.get("search")

    if search:

        tasks = tasks.filter(
            title__icontains=search
        )

    # ----------------------------------
    # Status Filter
    # ----------------------------------

    status = request.GET.get("status")

    if status:

        tasks = tasks.filter(
            status=status
        )

    # ----------------------------------
    # Priority Filter
    # ----------------------------------

    priority = request.GET.get("priority")

    if priority:

        tasks = tasks.filter(
            priority=priority
        )

    # ----------------------------------
    # Due Date Filter
    # ----------------------------------

    due_date = request.GET.get("due_date")

    if due_date:

        tasks = tasks.filter(
            due_date=due_date
        )

    # ----------------------------------
    # Pagination
    # ----------------------------------

    paginator = Paginator(
        tasks,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    # ----------------------------------
    # Today's Date
    # ----------------------------------

    today = timezone.now().date()

    return render(
        request,
        "tasks/task_list.html",
        {
            "tasks": page_obj,
            "page_obj": page_obj,
            "today": today,
            "priority_choices": Task.PRIORITY_CHOICES,
            "status_choices": Task.STATUS_CHOICES,
        },
    )
# ==========================================================
# CREATE TASK
# ==========================================================

class TaskCreateView(LoginRequiredMixin, CreateView):

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):

        # Agent can assign task only to themselves
        if self.request.user.role != "admin":
            form.instance.assigned_to = self.request.user

        try:

            with transaction.atomic():

                response = super().form_valid(form)

            messages.success(
                self.request,
                "Task created successfully."
            )

            return response

        except Exception:

            messages.error(
                self.request,
                "Unable to create task."
            )

            return self.form_invalid(form)


# ==========================================================
# UPDATE TASK
# ==========================================================

class TaskUpdateView(LoginRequiredMixin, UpdateView):

    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

    def get_queryset(self):

        if self.request.user.role == "admin":

            return Task.objects.select_related(
                "assigned_to",
                "related_contact",
                "related_lead",
            )

        return Task.objects.select_related(
            "assigned_to",
            "related_contact",
            "related_lead",
        ).filter(
            assigned_to=self.request.user
        )

    def form_valid(self, form):

        # Prevent agents from reassigning tasks
        if self.request.user.role != "admin":
            form.instance.assigned_to = self.request.user

        try:

            with transaction.atomic():

                response = super().form_valid(form)

            messages.success(
                self.request,
                "Task updated successfully."
            )

            return response

        except Exception:

            messages.error(
                self.request,
                "Unable to update task."
            )

            return self.form_invalid(form)
# ==========================================================
# TASK DETAIL
# ==========================================================

@login_required
def task_detail(request, pk):

    task = get_object_or_404(
        Task.objects.select_related(
            "assigned_to",
            "related_contact",
            "related_lead",
        ),
        pk=pk,
    )

    # Permission Check
    if (
        request.user.role != "admin"
        and task.assigned_to != request.user
    ):

        messages.error(
            request,
            "You don't have permission to view this task."
        )

        return redirect(
            "tasks:task_list"
        )

    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task,
        },
    )


# ==========================================================
# MARK TASK AS COMPLETE
# ==========================================================

@login_required
def task_complete(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
    )

    # Permission Check
    if (
        request.user.role != "admin"
        and task.assigned_to != request.user
    ):

        messages.error(
            request,
            "Permission denied."
        )

        return redirect(
            "tasks:task_list"
        )

    try:

        with transaction.atomic():

            task.status = "done"
            task.save()

        messages.success(
            request,
            "Task marked as completed."
        )

    except Exception:

        messages.error(
            request,
            "Unable to complete task."
        )

    return redirect(
        "tasks:task_list"
    )


# ==========================================================
# DELETE TASK
# ==========================================================

@login_required
def task_delete(request, pk):

    task = get_object_or_404(
        Task.objects.select_related(
            "assigned_to",
            "related_contact",
            "related_lead",
        ),
        pk=pk,
    )

    # Permission Check
    if (
        request.user.role != "admin"
        and task.assigned_to != request.user
    ):

        messages.error(
            request,
            "Permission denied."
        )

        return redirect(
            "tasks:task_list"
        )

    if request.method == "POST":

        try:

            with transaction.atomic():

                task.delete()

            messages.success(
                request,
                "Task deleted successfully."
            )

            return redirect(
                "tasks:task_list"
            )

        except Exception:

            messages.error(
                request,
                "Unable to delete task."
            )

    return render(
        request,
        "tasks/task_confirm_delete.html",
        {
            "task": task,
        },
    )