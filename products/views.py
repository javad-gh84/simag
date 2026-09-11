from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.contrib import messages
from .models import Product, Category, Wishlist

def home(request):
    products = Product.objects.filter(is_active=True, is_featured=True)[:12]
    categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count('products', filter=Q(products__is_active=True))
    )
    return render(request, 'products/home.html', {
        'products': products,
        'categories': categories
    })

def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True, parent__isnull=True).annotate(
        product_count=Count('products', filter=Q(products__is_active=True))
    )

    category_slug = request.GET.get('category')
    category = None
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug, is_active=True)
            products = products.filter(category=category)
        except Category.DoesNotExist:
            category = None
            products = Product.objects.filter(is_active=True)

    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'category': category,
        'search_query': search_query
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    variants = product.variants.all()
    images = product.images.all()

    is_in_wishlist = False
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        is_in_wishlist = wishlist.products.filter(id=product.id).exists()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'variants': variants,
        'images': images,
        'is_in_wishlist': is_in_wishlist,
    })


def contact(request):
    if request.method == 'POST':
        messages.success(request, '✅ پیام شما با موفقیت ارسال شد!')
        return redirect('products:contact')
    return render(request, 'products/contact.html')


def about(request):
    return render(request, 'products/about.html')


def custom_404(request, exception):
    suggested_products = Product.objects.filter(is_active=True)[:4]
    return render(request, '404.html', {
        'suggested_products': suggested_products
    }, status=404)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    variants = product.variants.all()
    images = product.images.all()

    is_in_wishlist = False
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        is_in_wishlist = wishlist.products.filter(id=product.id).exists()

    # ===== محصولات مرتبط =====
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'variants': variants,
        'images': images,
        'is_in_wishlist': is_in_wishlist,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

def robots_txt(request):
    return render(request, 'robots.txt', {}, content_type='text/plain')