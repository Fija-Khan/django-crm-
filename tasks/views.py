from django.contrib.auth.decorators import login_required
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

    return render(request, "tasks/task_list.html", {"tasks": tasks})


# ---------------------------
# CREATE TASK
# ---------------------------
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        # 🔥 CRM LOGIC FIX:
        # If admin creates task but doesn't assign -> optional fallback
        if not form.instance.assigned_to:
            form.instance.assigned_to = self.request.user

        return super().form_valid(form)


# ---------------------------
# UPDATE TASK
# ---------------------------
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        # 🔐 Security Fix (important)
        user = self.request.user

        if user.role == "admin":
            return Task.objects.all()

        return Task.objects.filter(assigned_to=user)


# ---------------------------
# MARK TASK COMPLETE
# ---------------------------
@login_required
def task_complete(request, pk):

    task = get_object_or_404(Task, pk=pk)

    # 🔐 Permission check fix
    if request.user.role != "admin" and task.assigned_to != request.user:
        return redirect("task_list")

    task.status = "done"
    task.save()

    return redirect("task_list")