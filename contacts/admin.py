from django.contrib import admin
from .models import Company, Contact

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'website')
    search_fields = ('name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'company', 'assigned_to', 'source')
    list_filter = ('source', 'assigned_to')
    search_fields = ('first_name', 'last_name', 'email')
