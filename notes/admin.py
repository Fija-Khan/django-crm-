from django.contrib import admin

from .models import Note



@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):

    list_display = (
        "created_by",
        "contact",
        "lead",
        "created_at",
    )


    list_filter = (
        "created_at",
    )


    search_fields = (
        "content",
        "contact__first_name",
        "contact__last_name",
        "lead__name",
        "created_by__username",
    )


    ordering = (
        "-created_at",
    )


    list_per_page = 20