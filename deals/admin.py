from django.contrib import admin
from .models import Deal

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('lead', 'amount', 'stage', 'close_date')
    ist_filter = ('stage',)