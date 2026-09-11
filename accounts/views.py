import re
import random
import json
from datetime import timedelta
from sms.utils import send_otp_code
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import authenticate

from .models import User, OTPCode
from products.models import Product, Category, Wishlist, ProductImage, ProductVariant
from orders.models import Order, OrderItem
from cart.models import Cart
from .forms import RegisterForm, UserUpdateForm, CustomPasswordChangeForm


# ============================================================
#                      توابع کمکی
# ============================================================

def is_valid_iranian_phone(phone):
    pattern = r'^(0|0098|\+98)9[0-9]{9}$'
    return re.match(pattern, phone) is not None


def send_otp(user):
    code = str(random.randint(100000, 999999))
    OTPCode.objects.create(user=user, code=code)
    
    result = send_otp_code(user.phone, code)
    
    if result['success']:
        print(f"✅ کد OTP با موفقیت ارسال شد: {code}")
    else:
        print(f"❌ خطا در ارسال OTP: {result['message']}")
        print(f"📱 کد OTP برای {user.phone}: {code}")
    
    return code


# ============================================================
#                      احراز هویت کاربر
# ============================================================

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.username = f"user_{form.cleaned_data['phone']}"
            user.save()
            send_otp(user)
            request.session['login_user_id'] = user.id
            messages.success(request, '✅ ثبت‌نام موفق! کد تأیید ارسال شد.')
            return redirect('accounts:verify')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        try:
            user = User.objects.get(phone=identifier)
            send_otp(user)
            request.session['login_user_id'] = user.id
            messages.success(request, '📱 کد تأیید ارسال شد.')
            return redirect('accounts:verify')
        except User.DoesNotExist:
            messages.error(request, '❌ کاربری با این شماره یافت نشد.')
    return render(request, 'accounts/login.html')


def verify_view(request):
    if request.method == 'POST':
        user_id = request.session.get('login_user_id')
        if not user_id:
            return redirect('accounts:login')
        user = User.objects.get(id=user_id)
        code = request.POST.get('code')
        try:
            otp = OTPCode.objects.filter(user=user, code=code, is_used=False).latest('created_at')
            if otp.is_valid():
                otp.is_used = True
                otp.save()
                user.is_verified = True
                user.save()
                login(request, user)
                messages.success(request, f'✅ خوش آمدید {user.full_name or user.phone}!')
                return redirect('products:home')
            else:
                messages.error(request, '❌ کد منقضی شده یا نامعتبر است.')
        except OTPCode.DoesNotExist:
            messages.error(request, '❌ کد وارد شده صحیح نیست.')
    return render(request, 'accounts/verify.html')


def resend_view(request):
    user_id = request.session.get('login_user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        send_otp(user)
        return JsonResponse({'success': True, 'message': 'کد جدید ارسال شد'})
    return JsonResponse({'success': False, 'message': 'خطا در ارسال کد'})


def logout_view(request):
    logout(request)
    messages.success(request, '👋 شما با موفقیت خارج شدید.')
    return redirect('products:home')


# ============================================================
#                      احراز هویت ادمین
# ============================================================

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('accounts:admin_dashboard')
    
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(phone=phone)
            if user.check_password(password):
                if user.is_staff:
                    # 🔥 این خط مهمه: backend رو مشخص کن
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request, f'✅ خوش آمدید {user.full_name or user.phone}!')
                    return redirect('accounts:admin_dashboard')
                else:
                    messages.error(request, '❌ شما دسترسی ادمین ندارید!')
            else:
                messages.error(request, '❌ رمز عبور اشتباه است.')
        except User.DoesNotExist:
            messages.error(request, '❌ کاربری با این شماره یافت نشد.')
    
    return render(request, 'accounts/admin_login.html')


def admin_logout_view(request):
    logout(request)
    messages.success(request, '👋 شما با موفقیت خارج شدید.')
    return redirect('accounts:admin_login')


# ============================================================
#                      پنل کاربری
# ============================================================

@login_required
def user_dashboard(request):
    user = request.user
    total_orders = Order.objects.filter(user=user).count()
    total_spent = Order.objects.filter(user=user, status='delivered').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_orders = Order.objects.filter(user=user, status='pending').count()
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    wishlist_count = wishlist.products.count()
    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    suggested_products = Product.objects.filter(is_active=True)[:4]
    context = {
        'user': user,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'pending_orders': pending_orders,
        'wishlist_count': wishlist_count,
        'recent_orders': recent_orders,
        'suggested_products': suggested_products,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'accounts/order_detail.html', {'order': order})


@login_required
def user_wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'accounts/wishlist.html', {'wishlist': wishlist})


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    messages.success(request, f'✅ {product.name} به علاقه‌مندی‌ها اضافه شد!')
    return redirect('products:product_detail', slug=product.slug)


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    messages.success(request, f'🗑️ {product.name} از علاقه‌مندی‌ها حذف شد!')
    return redirect('accounts:wishlist')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ اطلاعات با موفقیت به‌روزرسانی شد!')
            return redirect('accounts:dashboard')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '✅ رمز عبور با موفقیت تغییر کرد!')
            return redirect('accounts:dashboard')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


# ============================================================
#                      داشبورد مدیریت
# ============================================================

def admin_dashboard(request):
    # ===== بررسی دسترسی =====
    if not request.user.is_authenticated:
        return redirect('accounts:admin_login')
    
    if not request.user.is_staff:
        messages.error(request, '❌ شما دسترسی ادمین ندارید!')
        return redirect('products:home')
    
    # ===== آمار کلی =====
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_products = Product.objects.filter(is_active=True).count()
    total_categories = Category.objects.filter(is_active=True).count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # ===== آمار امروز =====
    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today).count()
    today_revenue = Order.objects.filter(created_at__date=today, status='delivered').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # ===== سفارشات در انتظار =====
    pending_orders = Order.objects.filter(status='pending').count()
    
    # ===== آخرین سفارشات =====
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    
    # ===== کاربران جدید =====
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # ===== وضعیت سفارشات =====
    status_counts = {
        'pending': Order.objects.filter(status='pending').count(),
        'processing': Order.objects.filter(status='processing').count(),
        'shipped': Order.objects.filter(status='shipped').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }
    
    # ===== فروش ماهانه =====
    monthly_sales = []
    for i in range(6, -1, -1):
        date = timezone.now().date() - timedelta(days=30*i)
        month_start = date.replace(day=1)
        if i == 0:
            month_end = timezone.now().date()
        else:
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        revenue = Order.objects.filter(
            status='delivered',
            created_at__date__gte=month_start,
            created_at__date__lte=month_end
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        monthly_sales.append({
            'month': month_start.strftime('%b'),
            'revenue': revenue,
        })
    
    context = {
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'total_categories': total_categories,
        'total_revenue': total_revenue,
        'today_orders': today_orders,
        'today_revenue': today_revenue,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
        'status_counts': status_counts,
        'monthly_sales': monthly_sales,
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)


# ============================================================
#                      مدیریت سفارشات
# ============================================================

@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'accounts/admin_orders.html', {'orders': orders})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, '✅ وضعیت سفارش با موفقیت تغییر کرد!')
        return redirect('accounts:admin_order_detail', order_id=order.id)
    return render(request, 'accounts/admin_order_detail.html', {'order': order})


@staff_member_required
def admin_order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, '🗑️ سفارش با موفقیت حذف شد!')
        return redirect('accounts:admin_orders')
    return render(request, 'accounts/admin_order_delete.html', {'order': order})


# ============================================================
#                      مدیریت کاربران
# ============================================================

@staff_member_required
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/admin_users.html', {'users': users})


@staff_member_required
def admin_user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        is_active = request.POST.get('is_active') == 'on'
        is_staff = request.POST.get('is_staff') == 'on'
        user.is_active = is_active
        user.is_staff = is_staff
        user.save()
        messages.success(request, '✅ وضعیت کاربر با موفقیت تغییر کرد!')
        return redirect('accounts:admin_user_detail', user_id=user.id)
    return render(request, 'accounts/admin_user_detail.html', {'user': user})


@staff_member_required
def admin_user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, '🗑️ کاربر با موفقیت حذف شد!')
        return redirect('accounts:admin_users')
    return render(request, 'accounts/admin_user_delete.html', {'user': user})


# ============================================================
#                      مدیریت محصولات
# ============================================================

@staff_member_required
def admin_products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'accounts/admin_products.html', {'products': products})


@staff_member_required
def admin_product_add(request):
    categories = Category.objects.filter(is_active=True)
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        brand = request.POST.get('brand', '')
        material = request.POST.get('material', '')
        color = request.POST.get('color', '')
        volume = request.POST.get('volume', '')
        weight = request.POST.get('weight', '')
        is_active = request.POST.get('is_active') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        
        if name and category_id and price:
            category = get_object_or_404(Category, id=category_id)
            
            if not slug or slug.strip() == '':
                from django.utils.text import slugify
                base_slug = slugify(name)
                slug = base_slug
                counter = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
            
            product = Product.objects.create(
                name=name,
                slug=slug,
                category=category,
                price=price,
                description=description,
                brand=brand,
                material=material,
                color=color,
                volume=volume,
                weight=weight,
                is_active=is_active,
                is_featured=is_featured
            )
            
            images = request.FILES.getlist('images')
            for i, img in enumerate(images):
                ProductImage.objects.create(
                    product=product,
                    image=img,
                    is_main=(i == 0),
                    order=i
                )
            
            messages.success(request, '✅ محصول با موفقیت اضافه شد!')
            return redirect('accounts:admin_products')
        else:
            messages.error(request, '❌ لطفاً تمام فیلدهای ضروری را پر کنید.')
    
    return render(request, 'accounts/admin_product_add.html', {'categories': categories})


@staff_member_required
def admin_product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.filter(is_active=True)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.slug = request.POST.get('slug')
        product.category_id = request.POST.get('category')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.brand = request.POST.get('brand', '')
        product.material = request.POST.get('material', '')
        product.color = request.POST.get('color', '')
        product.volume = request.POST.get('volume', '')
        product.weight = request.POST.get('weight', '')
        product.is_active = request.POST.get('is_active') == 'on'
        product.is_featured = request.POST.get('is_featured') == 'on'
        
        if not product.slug or product.slug.strip() == '':
            from django.utils.text import slugify
            product.slug = slugify(product.name)
        
        product.save()
        messages.success(request, '✅ محصول با موفقیت ویرایش شد!')
        return redirect('accounts:admin_products')
    
    return render(request, 'accounts/admin_product_edit.html', {
        'product': product,
        'categories': categories
    })


@staff_member_required
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, '🗑️ محصول با موفقیت حذف شد!')
        return redirect('accounts:admin_products')
    return render(request, 'accounts/admin_product_delete.html', {'product': product})


@staff_member_required
def admin_product_image_delete(request, image_id):
    image = get_object_or_404(ProductImage, id=image_id)
    product_id = image.product.id
    image.delete()
    messages.success(request, '🗑️ عکس با موفقیت حذف شد!')
    return redirect('accounts:admin_product_edit', product_id=product_id)


# ============================================================
#                      مدیریت دسته‌بندی
# ============================================================

@staff_member_required
def admin_categories(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'accounts/admin_categories.html', {'categories': categories})


@staff_member_required
def admin_category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        is_active = request.POST.get('is_active') == 'on'
        image = request.FILES.get('image')
        
        if name:
            category = Category.objects.create(
                name=name,
                is_active=is_active,
                image=image
            )
            messages.success(request, '✅ دسته‌بندی با موفقیت اضافه شد!')
            return redirect('accounts:admin_categories')
        else:
            messages.error(request, '❌ لطفاً نام دسته‌بندی را وارد کنید.')
    
    return render(request, 'accounts/admin_category_add.html')


@staff_member_required
def admin_category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.is_active = request.POST.get('is_active') == 'on'
        
        if request.FILES.get('image'):
            if category.image:
                category.image.delete()
            category.image = request.FILES.get('image')
        
        category.save()
        messages.success(request, '✅ دسته‌بندی با موفقیت ویرایش شد!')
        return redirect('accounts:admin_categories')
    
    return render(request, 'accounts/admin_category_edit.html', {'category': category})


@staff_member_required
def admin_category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        if category.image:
            category.image.delete()
        category.delete()
        messages.success(request, '🗑️ دسته‌بندی با موفقیت حذف شد!')
        return redirect('accounts:admin_categories')
    return render(request, 'accounts/admin_category_delete.html', {'category': category})