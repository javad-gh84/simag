from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price_display', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__phone', 'user__full_name']
    readonly_fields = ['created_at', 'updated_at']
    
    def total_items(self, obj):
        return obj.total_items
    total_items.short_description = 'تعداد محصولات'
    
    def total_price_display(self, obj):
        return f"{obj.total_price:,.0f} تومان"
    total_price_display.short_description = 'قیمت کل'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price_display', 'created_at']
    list_filter = ['created_at']
    search_fields = ['cart__user__phone', 'product__name']
    readonly_fields = ['created_at', 'updated_at']
    
    def total_price_display(self, obj):
        return f"{obj.total_price:,.0f} تومان"
    total_price_display.short_description = 'قیمت'