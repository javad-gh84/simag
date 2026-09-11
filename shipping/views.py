from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import Shipment
from .services import send_to_tipax, send_to_post

@login_required
def ship_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if order.status != 'paid':
        messages.error(request, 'این سفارش هنوز پرداخت نشده است.')
        return redirect('orders:order_detail', order_number=order_number)
    
    # دریافت روش ارسال از سفارش
    if order.shipping_method == 'tipax':
        tracking_code = send_to_tipax(order, order.address)
    else:
        tracking_code = send_to_post(order, order.address)
    
    # ایجاد یا بروزرسانی شیپمنت
    shipment, created = Shipment.objects.get_or_create(order=order)
    shipment.tracking_code = tracking_code
    shipment.shipping_method = order.shipping_method
    shipment.status = 'shipped'
    shipment.save()
    
    # بروزرسانی وضعیت سفارش
    order.status = 'shipped'
    order.tracking_code = tracking_code
    order.save()
    
    messages.success(request, f'سفارش ارسال شد. کد رهگیری: {tracking_code}')
    return redirect('orders:order_detail', order_number=order_number)