from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'role',
        'is_approved',
        'is_active',
        'is_staff',
    )

    list_filter = (
        'role',
        'is_approved',
        'is_active',
        'is_staff',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('CRM Info', {
            'fields': (
                'role',
                'phone',
                'profile_pic',
                'is_approved',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('CRM Info', {
            'fields': (
                'email',
                'role',
                'phone',
                'profile_pic',
                'is_active',
                'is_approved',
            )
        }),
    )