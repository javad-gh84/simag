from django.urls import path
from . import views

app_name = 'barcode'

urlpatterns = [
    path('scan/', views.scan_barcode, name='scan_barcode'),
    path('increase/', views.increase_stock, name='increase_stock'),
]