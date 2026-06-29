from django.contrib import admin
from .models import Lead, LeadActivity

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('title', 'contact', 'status', 'assigned_to', 'estimated_value' )
    list_filter = ('status', 'assigned_to')

@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin):
    list_display = ('lead','old_status', 'new_status', 'changed_by', 'changed_at')
    readonly_fields = ( 'lead', 'old_status', 'new_status', 'changed_by', 'changed_at')
    
