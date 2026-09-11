from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # ===== کاربری =====
    path('', views.order_list, name='order_list'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.create_order, name='create_order'),
    path('checkout/', views.checkout, name='checkout'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('track/<int:order_id>/', views.track_order, name='track_order'),
    
    # ===== گزارشات (ادمین) =====
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/products/', views.product_report, name='product_report'),
    path('reports/users/', views.user_report, name='user_report'),
    path('reports/export/', views.export_excel, name='export_excel'),
]