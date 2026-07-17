from django.shortcuts import render, redirect, get_object_or_404
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
            request=request,
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
                "Your account is inactive. Please contact the administrator."
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

            # Remove this line if your model doesn't have is_approved
            if hasattr(user, "is_approved"):
                user.is_approved = False

            user.save()

            messages.success(
                request,
                "Registration submitted successfully. Please wait for admin approval."
            )

            return redirect("login")

        messages.error(
            request,
            "Please correct the errors below."
        )

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

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
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
# ADMIN PANEL - DASHBOARD
# ==========================================

@login_required
def admin_dashboard(request):

    if request.user.role != "admin":

        messages.error(
            request,
            "You don't have permission to access this page."
        )

        return redirect("dashboard")

    context = {

        "total_users": CustomUser.objects.count(),

        "active_users": CustomUser.objects.filter(
            is_active=True
        ).count(),

        "inactive_users": CustomUser.objects.filter(
            is_active=False
        ).count(),

        "admin_users": CustomUser.objects.filter(
            role="admin"
        ).count(),

        "agent_users": CustomUser.objects.filter(
            role="agent"
        ).count(),

        "total_contacts": Contact.objects.count(),

        "total_leads": Lead.objects.count(),

        "total_deals": Deal.objects.count(),

        "total_tasks": Task.objects.count(),

        "recent_users": CustomUser.objects.order_by(
            "-date_joined"
        )[:5],

    }

    return render(
        request,
        "admin_panel/dashboard.html",
        context,
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

        if search:

            queryset = queryset.filter(

                Q(username__icontains=search) |

                Q(first_name__icontains=search) |

                Q(last_name__icontains=search) |

                Q(email__icontains=search)

            )

        if role:

            queryset = queryset.filter(
                role=role
            )

        if status == "active":

            queryset = queryset.filter(
                is_active=True
            )

        elif status == "inactive":

            queryset = queryset.filter(
                is_active=False
            )

        return queryset


    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )

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

        context["total_users"] = CustomUser.objects.count()

        context["total_admins"] = CustomUser.objects.filter(
            role="admin"
        ).count()

        context["total_agents"] = CustomUser.objects.filter(
            role="agent"
        ).count()

        return context
# ==========================================
# ADMIN PANEL - DASHBOARD
# ==========================================

@login_required
def admin_dashboard(request):

    if request.user.role != "admin":

        messages.error(
            request,
            "You don't have permission to access this page."
        )

        return redirect("dashboard")

    context = {

        "total_users": CustomUser.objects.count(),

        "active_users": CustomUser.objects.filter(
            is_active=True
        ).count(),

        "inactive_users": CustomUser.objects.filter(
            is_active=False
        ).count(),

        "admin_users": CustomUser.objects.filter(
            role="admin"
        ).count(),

        "agent_users": CustomUser.objects.filter(
            role="agent"
        ).count(),

        "total_contacts": Contact.objects.count(),

        "total_leads": Lead.objects.count(),

        "total_deals": Deal.objects.count(),

        "total_tasks": Task.objects.count(),

        "recent_users": CustomUser.objects.order_by(
            "-date_joined"
        )[:5],

    }

    return render(
        request,
        "admin_panel/dashboard.html",
        context,
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

        if search:

            queryset = queryset.filter(

                Q(username__icontains=search) |

                Q(first_name__icontains=search) |

                Q(last_name__icontains=search) |

                Q(email__icontains=search)

            )

        if role:

            queryset = queryset.filter(
                role=role
            )

        if status == "active":

            queryset = queryset.filter(
                is_active=True
            )

        elif status == "inactive":

            queryset = queryset.filter(
                is_active=False
            )

        return queryset


    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )

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

        context["total_users"] = CustomUser.objects.count()

        context["total_admins"] = CustomUser.objects.filter(
            role="admin"
        ).count()

        context["total_agents"] = CustomUser.objects.filter(
            role="agent"
        ).count()

        return context
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

    def form_invalid(self, form):

        messages.error(
            self.request,
            "Please correct the errors below."
        )

        return super().form_invalid(form)


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

    def form_invalid(self, form):

        messages.error(
            self.request,
            "Please correct the errors below."
        )

        return super().form_invalid(form)


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
