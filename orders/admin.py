from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'is_offline']
    search_fields = ['order_number', 'user__phone', 'tracking_code']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not obj.order_number:
            import random
            obj.order_number = f"SMG-{random.randint(100000, 999999)}"
        super().save_model(request, obj, form, change)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total_price']
    search_fields = ['product__name', 'order__order_number']