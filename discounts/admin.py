from django.contrib import admin
from .models import DiscountCode

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'value', 'max_usage', 'used_count', 'is_active']
    list_filter = ['discount_type', 'is_active']