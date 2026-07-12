from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # -----------------------------
    # Admin Panel
    # -----------------------------
    path('admin/', admin.site.urls),

    # -----------------------------
    # Authentication
    # -----------------------------
    path('accounts/', include('accounts.urls')),

    # Password Reset
    path(
        'accounts/password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'accounts/password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'accounts/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # -----------------------------
    # Dashboard
    # -----------------------------
    path('', include('dashboard.urls')),

    # -----------------------------
    # Contacts
    # -----------------------------
    path('contacts/', include('contacts.urls')),

    # -----------------------------
    # Leads
    # -----------------------------
    path('leads/', include('leads.urls')),

    # -----------------------------
    # Deals
    # -----------------------------
    path('deals/', include('deals.urls')),

    # -----------------------------
    # Tasks
    # -----------------------------
    path('tasks/', include('tasks.urls')),

    # -----------------------------
    # Interactions
    # -----------------------------
    path('interactions/', include('interactions.urls')),

    # -----------------------------
    # Notes
    # -----------------------------
    path('notes/', include('notes.urls')),
]


# -----------------------------
# Media Files
# -----------------------------
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )