from django.contrib import admin
from .models import Interaction


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):

    list_display = (
        "contact",
        "interaction_type",
        "logged_by",
        "interaction_date",
    )

    list_filter = (
        "interaction_type",
        "interaction_date",
    )

    search_fields = (
        "contact__first_name",
        "contact__last_name",
        "contact__email",
        "summary",
    )

    ordering = (
        "-interaction_date",
    )

    list_per_page = 20

    date_hierarchy = "interaction_date"