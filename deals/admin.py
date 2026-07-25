from django.contrib import admin
from .models import Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):

    list_display = (
        'lead',
        'amount',
        'stage',
        'close_date',
        'created_at',
    )


    list_filter = (
        'stage',
        'close_date',
        'created_at',
    )


    search_fields = (
        'lead__title',
        'lead__contact__name',
        'lead__contact__email',
    )


    readonly_fields = (
        'created_at',
    )


    ordering = (
        '-created_at',
    )


    list_per_page = 20