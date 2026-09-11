from django.urls import path
from . import views

app_name = 'shipping'

urlpatterns = [
    path('ship/<str:order_number>/', views.ship_order, name='ship_order'),
]