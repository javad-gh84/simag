from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, OTPCode

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['phone', 'full_name', 'email', 'is_verified', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_verified', 'date_joined']
    search_fields = ['phone', 'full_name', 'email']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('full_name', 'email', 'address', 'postal_code')}),
        ('وضعیت', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('گروه‌ها و دسترسی‌ها', {'fields': ('groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'created_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__phone', 'code']
    readonly_fields = ['created_at']
    ordering = ['-created_at']