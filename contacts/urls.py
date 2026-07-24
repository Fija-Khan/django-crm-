from django.urls import path
from . import views

from .views import (
    ContactCreateView,
    ContactDetailView,
    ContactUpdateView,
    ContactDeleteView,
    CompanyCreateView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyDeleteView,
)

app_name = "contacts"

urlpatterns = [

    # ==========================================
    # CONTACT URLS
    # ==========================================

    path("", views.contact_list, name="contact_list"),

    path("add/", ContactCreateView.as_view(), name="contact_add"),

    path("<int:pk>/", ContactDetailView.as_view(), name="contact_detail"),

    path("<int:pk>/edit/", ContactUpdateView.as_view(), name="contact_edit"),

    path("<int:pk>/delete/", ContactDeleteView.as_view(), name="contact_delete"),

    path("import/", views.contact_import, name="contact_import"),

    path("export/", views.contact_export, name="contact_export"),


    # ==========================================
    # COMPANY URLS
    # ==========================================

    path("companies/", views.company_list, name="company_list"),

    path("companies/add/", CompanyCreateView.as_view(), name="company_add"),

    path("companies/<int:pk>/", CompanyDetailView.as_view(), name="company_detail"),

    path("companies/<int:pk>/edit/", CompanyUpdateView.as_view(), name="company_edit"),

    path("companies/<int:pk>/delete/", CompanyDeleteView.as_view(), name="company_delete"),
]