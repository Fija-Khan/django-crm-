from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import CustomUser
from .forms import (
    RegisterForm,
    UserCreateForm,
    UserUpdateForm,)
from contacts.models import Contact
from leads.models import Lead
from deals.models import Deal
from tasks.models import Task


# ==========================================
# ADMIN ACCESS MIXIN
# ==========================================

class AdminRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == "admin"
        )

    def handle_no_permission(self):

        messages.error(
            self.request,
            "You don't have permission to access this page."
        )

        return redirect("dashboard")


# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect("login")

        if not user.is_active:

            messages.error(
                request,
                "Your account is waiting for admin approval."
            )

            return redirect("login")

        login(request, user)

        messages.success(
            request,
            f"Welcome, {user.username}!"
        )

        return redirect("dashboard")

    return render(
        request,
        "accounts/login.html",
    )


# ==========================================
# LOGOUT
# ==========================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")


# ==========================================
# REGISTER
# ==========================================

def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.role = "agent"
            user.is_active = False
            user.is_approved = False

            user.save()

            messages.success(
                request,
                "Registration successful. Please wait for admin approval."
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


# ==========================================
# PROFILE
# ==========================================

@login_required
def profile_view(request):

    user = request.user

    if request.method == "POST":

        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        if request.FILES.get("profile_pic"):

            user.profile_pic = request.FILES["profile_pic"]

        user.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    return render(
        request,
        "accounts/profile.html",
        {
            "user": user,
        },
    )


# ==========================================
# ADMIN PANEL - USER LIST
# ==========================================

class UserListView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    ListView,
):

    model = CustomUser
    template_name = "admin_panel/user_list.html"
    context_object_name = "users"

    def get_queryset(self):

        return CustomUser.objects.order_by("username")


# ==========================================
# ADMIN PANEL - CREATE USER
# ==========================================

class UserCreateView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    CreateView,
):

    model = CustomUser
    form_class = UserCreateForm
    template_name = "admin_panel/user_form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "User created successfully."
        )

        return super().form_valid(form)


# ==========================================
# ADMIN PANEL - UPDATE USER
# ==========================================

class UserUpdateView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    UpdateView,
):

    model = CustomUser
    form_class = UserUpdateForm
    template_name = "admin_panel/user_form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "User updated successfully."
        )

        return super().form_valid(form)


# ==========================================
# ADMIN PANEL - DELETE USER
# ==========================================

class UserDeleteView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    DeleteView,
):

    model = CustomUser
    template_name = "admin_panel/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")

    def delete(self, request, *args, **kwargs):

        messages.success(
            request,
            "User deleted successfully."
        )

        return super().delete(request, *args, **kwargs)