from django.urls import path

from .views import (
    login_view,
    logout_view,
    register,
    profile_view,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)

urlpatterns = [

    # -----------------------------
    # Authentication
    # -----------------------------
    path(
        "login/",
        login_view,
        name="login",
    ),

    path(
        "logout/",
        logout_view,
        name="logout",
    ),

    path(
        "register/",
        register,
        name="register",
    ),

    path(
        "profile/",
        profile_view,
        name="profile",
    ),

    # -----------------------------
    # Admin Panel - User Management
    # -----------------------------
    path(
        "admin-panel/users/",
        UserListView.as_view(),
        name="user_list",
    ),

    path(
        "admin-panel/users/add/",
        UserCreateView.as_view(),
        name="user_add",
    ),

    path(
        "admin-panel/users/<int:pk>/edit/",
        UserUpdateView.as_view(),
        name="user_edit",
    ),

    path(
        "admin-panel/users/<int:pk>/delete/",
        UserDeleteView.as_view(),
        name="user_delete",
    ),

]