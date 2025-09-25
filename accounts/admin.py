from django.contrib import admin
from .models import (CEOProfile, EmployeeProfile, User, CategoryDepartment)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'national_code', 'phone_number', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'national_code', 'phone_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'national_code', 'role', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'national_code', 'role', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(CEOProfile)
admin.site.register(EmployeeProfile)
admin.site.register(CategoryDepartment)
