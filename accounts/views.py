from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import CustomUser
from .forms import (
    RegisterForm,
    UserCreateForm,
    UserUpdateForm,
)
from .decorators import admin_required, agent_required

from contacts.models import Contact
from leads.models import Lead
from deals.models import Deal
from tasks.models import Task


# ==================================================
# ADMIN REQUIRED MIXIN
# ==================================================

class AdminRequiredMixin(UserPassesTestMixin):
    """
    Allow only admin users to access class based views.
    """

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


# ==================================================
# LOGIN
# ==================================================

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
                "Your account is inactive."
            )
            return redirect("login")

        if hasattr(user, "is_approved") and not user.is_approved:
            messages.warning(
                request,
                "Your account is waiting for admin approval."
            )
            return redirect("login")

        login(request, user)

        messages.success(
            request,
            f"Welcome back, {user.username}!"
        )

        return redirect("dashboard")

    return render(
        request,
        "accounts/login.html"
    )


# ==================================================
# LOGOUT
# ==================================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")


# ==================================================
# REGISTER
# ==================================================

def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.role = "agent"
            user.is_active = True
            user.is_approved = False

            user.save()

            messages.success(
                request,
                "Registration submitted. Wait for admin approval."
            )

            return redirect("login")

    else:
        form = RegisterForm()
# ==================================================
# PROFILE
# ==================================================

@login_required
def profile_view(request):

    user = request.user

    if request.method == "POST":

        user.username = request.POST.get(
            "username",
            user.username
        )

        user.email = request.POST.get(
            "email",
            user.email
        )

        user.phone = request.POST.get(
            "phone",
            user.phone
        )

        # ==========================================
        # Upload Profile Picture
        # ==========================================

        if request.FILES.get("profile_pic"):

            image = request.FILES["profile_pic"]

            if image.size > 2 * 1024 * 1024:

                messages.error(
                    request,
                    "Image size must be less than 2 MB."
                )

                return redirect("profile")

            user.profile_pic = image

        # ==========================================
        # Remove Profile Picture
        # ==========================================

        if request.POST.get("remove_profile_pic"):

            if user.profile_pic:
                user.profile_pic.delete(save=False)

            user.profile_pic = None

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
            "user": user
        }
    )


# ==================================================
# ADMIN DASHBOARD
# ==================================================

@login_required
@admin_required
def admin_dashboard(request):

    context = {

        "total_users":
            CustomUser.objects.count(),

        "active_users":
            CustomUser.objects.filter(
                is_active=True
            ).count(),

        "pending_users":
            CustomUser.objects.filter(
                is_approved=False
            ).count(),

        "admin_users":
            CustomUser.objects.filter(
                role="admin"
            ).count(),

        "agent_users":
            CustomUser.objects.filter(
                role="agent"
            ).count(),

        "total_contacts":
            Contact.objects.count(),

        "total_leads":
            Lead.objects.count(),

        "total_deals":
            Deal.objects.count(),

        "total_tasks":
            Task.objects.count(),

        "recent_users":
            CustomUser.objects.order_by(
                "-date_joined"
            )[:5],

    }

    return render(
        request,
        "admin_panel/dashboard.html",
        context
    )


# ==================================================
# AGENT DASHBOARD
# ==================================================

@login_required
@agent_required
def agent_dashboard(request):

    context = {

        "total_contacts":
            Contact.objects.count(),

        "total_leads":
            Lead.objects.count(),

        "total_deals":
            Deal.objects.count(),

        "total_tasks":
            Task.objects.filter(
                assigned_to=request.user
            ).count(),

    }

    return render(
        request,
        "dashboard/agent_dashboard.html",
        context
    )
# ==================================================
# USER LIST
# ==================================================

class UserListView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    ListView
):

    model = CustomUser

    template_name = "admin_panel/user_list.html"

    context_object_name = "users"

    paginate_by = 10


    def get_queryset(self):

        queryset = CustomUser.objects.order_by(
            "-date_joined"
        )

        search = self.request.GET.get(
            "search"
        )

        role = self.request.GET.get(
            "role"
        )

        status = self.request.GET.get(
            "status"
        )

        # ==============================
        # Search
        # ==============================

        if search:

            queryset = queryset.filter(

                Q(username__icontains=search)
                |
                Q(email__icontains=search)
                |
                Q(phone__icontains=search)

            )

        # ==============================
        # Role Filter
        # ==============================

        if role:

            queryset = queryset.filter(
                role=role
            )

        # ==============================
        # Status Filter
        # ==============================

        if status == "active":

            queryset = queryset.filter(
                is_active=True
            )

        elif status == "inactive":

            queryset = queryset.filter(
                is_active=False
            )

        elif status == "pending":

            queryset = queryset.filter(
                is_approved=False
            )

        return queryset


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # ==============================
        # Summary Cards
        # ==============================

        context["total_users"] = CustomUser.objects.count()

        context["total_admins"] = CustomUser.objects.filter(
            role="admin"
        ).count()

        context["total_agents"] = CustomUser.objects.filter(
            role="agent"
        ).count()

        context["active_users"] = CustomUser.objects.filter(
            is_active=True
        ).count()

        context["inactive_users"] = CustomUser.objects.filter(
            is_active=False
        ).count()

        context["pending_users"] = CustomUser.objects.filter(
            is_approved=False
        ).count()

        # ==============================
        # Keep Search Values
        # ==============================

        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        context["selected_role"] = self.request.GET.get(
            "role",
            ""
        )

        context["selected_status"] = self.request.GET.get(
            "status",
            ""
        )

        return context
# ==================================================
# CREATE USER
# ==================================================

class UserCreateView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    CreateView
):

    model = CustomUser

    form_class = UserCreateForm

    template_name = "admin_panel/user_form.html"

    success_url = reverse_lazy(
        "user_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "User created successfully."
        )

        return super().form_valid(form)


# ==================================================
# UPDATE USER
# ==================================================

class UserUpdateView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    UpdateView
):

    model = CustomUser

    form_class = UserUpdateForm

    template_name = "admin_panel/user_form.html"

    success_url = reverse_lazy(
        "user_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "User updated successfully."
        )

        return super().form_valid(form)


# ==================================================
# DELETE USER
# ==================================================

class UserDeleteView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    DeleteView
):

    model = CustomUser

    template_name = "admin_panel/user_confirm_delete.html"

    success_url = reverse_lazy(
        "user_list"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "User deleted successfully."
        )

        return super().form_valid(form)