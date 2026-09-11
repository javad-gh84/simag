from django.contrib import admin
from .models import Shipment

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['order', 'shipping_method', 'tracking_code', 'status']
    list_filter = ['shipping_method', 'status']
    search_fields = ['order__order_number', 'tracking_code']