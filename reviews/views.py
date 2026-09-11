from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg
from products.models import Product
from .models import Review
from .forms import ReviewForm


@login_required
def add_review(request, product_id):
    """افزودن نظر جدید"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # بررسی اینکه کاربر قبلاً نظر داده یا نه
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.error(request, '❌ شما قبلاً برای این محصول نظر داده‌اید!')
        return redirect('products:product_detail', slug=product.slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, '✅ نظر شما با موفقیت ثبت شد و پس از تایید نمایش داده می‌شود!')
            return redirect('products:product_detail', slug=product.slug)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/add_review.html', {
        'product': product,
        'form': form
    })


@login_required
def edit_review(request, review_id):
    """ویرایش نظر"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product = review.product
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ نظر شما با موفقیت ویرایش شد!')
            return redirect('products:product_detail', slug=product.slug)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/edit_review.html', {
        'review': review,
        'form': form
    })


@login_required
def delete_review(request, review_id):
    """حذف نظر"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, '🗑️ نظر شما با موفقیت حذف شد!')
        return redirect('products:product_detail', slug=product_slug)
    
    return render(request, 'reviews/delete_review.html', {'review': review})


def get_product_reviews(request, product_id):
    """API دریافت نظرات محصول (AJAX)"""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.filter(is_approved=True)
    
    average_rating = product.reviews.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg'] or 0
    
    data = {
        'reviews': [
            {
                'user': review.user.full_name or review.user.phone,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.strftime('%Y/%m/%d %H:%M'),
                'stars': '★' * review.rating + '☆' * (5 - review.rating)
            }
            for review in reviews
        ],
        'average_rating': round(average_rating, 1),
        'total_reviews': reviews.count()
    }
    
    return JsonResponse(data)