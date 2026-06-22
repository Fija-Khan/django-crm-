from django.contrib import admin
from .models import Interaction

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('contact', 'type', 'logged_by', 'interaction_date')
    list_filter = ('type',)