from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    login_view,
    logout_view,
    register,
    profile_view,
    admin_dashboard,
    agent_dashboard,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)



urlpatterns = [

    # ==================================================
    # AUTHENTICATION
    # ==================================================

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



    # ==================================================
    # USER PROFILE
    # ==================================================

    path(
        "profile/",
        profile_view,
        name="profile",
    ),



    # ==================================================
    # DASHBOARDS
    # ==================================================

    path(
        "admin-dashboard/",
        admin_dashboard,
        name="admin_dashboard",
    ),


    path(
        "agent-dashboard/",
        agent_dashboard,
        name="agent_dashboard",
    ),





    # ==================================================
    # PASSWORD RESET
    # ==================================================

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="password_reset",
    ),



    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),



    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),



    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),





    # ==================================================
    # ADMIN PANEL - USER MANAGEMENT
    # ==================================================

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