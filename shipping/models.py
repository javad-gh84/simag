from django.conf import settings
from django.db import models
from orders.models import Order

class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipment')
    tracking_code = models.CharField(max_length=100, blank=True)
    shipping_method = models.CharField(max_length=50, choices=(('tipax', 'تیپاکس'), ('post', 'پست')))
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'در انتظار ارسال'),
            ('shipped', 'ارسال شده'),
            ('delivered', 'تحویل داده شده'),
            ('failed', 'ناموفق'),
        ),
        default='pending'
    )

    def __str__(self):
        return f"ارسال سفارش {self.order.order_number}"