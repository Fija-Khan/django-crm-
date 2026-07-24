from django.contrib import admin
from .models import Company, Contact


# ==========================================
# COMPANY ADMIN
# ==========================================

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "industry",
        "website",
        "created_at",
    )

    search_fields = (
        "name",
        "industry",
    )

    list_filter = (
        "industry",
        "created_at",
    )

    ordering = (
        "name",
    )

    list_per_page = 20


# ==========================================
# CONTACT ADMIN
# ==========================================

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "company",
        "assigned_to",
        "source",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
    )

    list_filter = (
        "source",
        "company",
        "assigned_to",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "company",
        "assigned_to",
    )

    list_per_page = 20