from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import DiscountCode
from cart.models import Cart

@login_required
def apply_discount(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            discount = DiscountCode.objects.get(code=code)
            if discount.is_valid():
                cart = Cart.objects.get(user=request.user)
                total = sum(item.variant.product.price + item.variant.price_adjustment for item in cart.items.all())
                
                if discount.discount_type == 'percentage':
                    discount_amount = int(total * discount.value / 100)
                else:
                    discount_amount = discount.value
                
                # ذخیره در سشن یا برگرداندن به صورت JSON
                request.session['discount_code'] = code
                request.session['discount_amount'] = discount_amount
                
                return JsonResponse({
                    'success': True,
                    'discount_amount': discount_amount,
                    'final_total': total - discount_amount
                })
            else:
                return JsonResponse({'success': False, 'error': 'کد تخفیف معتبر نیست.'})
        except DiscountCode.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'کد تخفیف وجود ندارد.'})
    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر.'})