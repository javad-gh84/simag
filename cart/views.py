from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from products.models import Product
from .models import Cart, CartItem

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.total_price
    discount = 0
    final_price = total_price - discount
    suggested_products = Product.objects.filter(is_active=True)[:3]

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'discount': discount,
        'final_price': final_price,
        'suggested_products': suggested_products,
    }
    return render(request, 'cart/cart_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'✅ {product.name} به سبد خرید اضافه شد!')
    return redirect('cart:cart_detail')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'🗑️ {product_name} از سبد خرید حذف شد!')
    return redirect('cart:cart_detail')


@login_required
def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity', 1)
        except:
            quantity = int(request.POST.get('quantity', 1))

        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'تعداد باید حداقل ۱ باشد'})

        cart_item.quantity = quantity
        cart_item.save()

        cart = Cart.objects.get(user=request.user)
        return JsonResponse({
            'success': True,
            'total_price': cart.total_price,
            'item_total': cart_item.total_price,
            'total_items': cart.total_items
        })

    return JsonResponse({'success': False, 'error': 'روش نامعتبر'})