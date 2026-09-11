from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from products.models import ProductVariant
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def scan_barcode(request):
    """کاهش موجودی با اسکن بارکد (فروش حضوری)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        barcode = data.get('barcode')
        
        try:
            variant = ProductVariant.objects.get(barcode=barcode)
            if variant.stock > 0:
                variant.stock -= 1
                variant.save()
                return JsonResponse({
                    'success': True,
                    'product': variant.product.name,
                    'color': variant.color,
                    'remaining_stock': variant.stock
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'موجودی این محصول به پایان رسیده است.'
                })
        except ProductVariant.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'بارکد نامعتبر است.'
            })
    
    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر.'})


@login_required
def increase_stock(request):
    """افزایش موجودی با اسکن بارکد (ورود به انبار)"""
    if request.method == 'POST':
        data = json.loads(request.body)
        barcode = data.get('barcode')
        quantity = data.get('quantity', 1)
        
        try:
            variant = ProductVariant.objects.get(barcode=barcode)
            variant.stock += quantity
            variant.save()
            return JsonResponse({
                'success': True,
                'product': variant.product.name,
                'new_stock': variant.stock
            })
        except ProductVariant.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'بارکد نامعتبر است.'
            })
    
    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر.'})