def get_collaborative_recommendations(user, num_recommendations=5):
    # Get all reviews
    reviews = Review.objects.all().values('user_id', 'product_id', 'rating')
    if not reviews:
        return Product.objects.all()[:num_recommendations]  # fallback

    df = pd.DataFrame(list(reviews))
    user_item_matrix = df.pivot(index='user_id', columns='product_id', values='rating').fillna(0)

    if user.id not in user_item_matrix.index:
        return Product.objects.all()[:num_recommendations]

    # Use KNN
    model = NearestNeighbors(n_neighbors=5, metric='cosine')
    model.fit(user_item_matrix.values)

    user_ratings = user_item_matrix.loc[user.id].values.reshape(1, -1)
    distances, indices = model.kneighbors(user_ratings)

    similar_users = user_item_matrix.index[indices.flatten()[1:]]  # exclude self

    recommended_products = set()
    for sim_user in similar_users:
        sim_ratings = user_item_matrix.loc[sim_user]
        highly_rated = sim_ratings[sim_ratings >= 4].index
        recommended_products.update(highly_rated)

    # Exclude already rated
    user_rated = set(df[df['user_id'] == user.id]['product_id'])
    recommended_products -= user_rated

    products = Product.objects.filter(id__in=recommended_products)[:num_recommendations]
    return products

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem, Review, Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from sklearn.neighbors import NearestNeighbors
import pandas as pd

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query)
    return render(request, 'store/product_list.html', {'products': products, 'query': query})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    recommendations = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:5]
    ai_recommendations = []
    if request.user.is_authenticated:
        ai_recommendations = get_collaborative_recommendations(request.user)
    reviews = product.reviews.all()
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating:
            Review.objects.create(product=product, user=request.user, rating=int(rating), comment=comment)
            messages.success(request, "Review added!")
            return redirect('product_detail', pk=pk)
    return render(request, 'store/product_detail.html', {'product': product, 'recommendations': recommendations, 'ai_recommendations': ai_recommendations, 'reviews': reviews})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f"{product.name} added to cart.")
    return redirect('product_detail', pk=pk)

@login_required
def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = Decimal(0)
    for pk, qty in cart.items():
        product = get_object_or_404(Product, pk=pk)
        subtotal = product.price * qty
        items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'store/cart.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')
    # Calculate total
    total = Decimal(0)
    items = []
    for pk, qty in cart.items():
        product = get_object_or_404(Product, pk=pk)
        total += product.price * qty
        items.append((product, qty))
    if request.method == 'POST':
        # Simulate payment success
        order = Order.objects.create(user=request.user, total=total, status='processing')
        for product, qty in items:
            OrderItem.objects.create(order=order, product=product, quantity=qty, price=product.price)
        request.session['cart'] = {}
        messages.success(request, "Payment successful! Order placed.")
        return redirect('order_detail', pk=order.pk)
    return render(request, 'store/checkout.html', {'total': total, 'items': items})

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f"{product.name} added to wishlist.")
    return redirect('product_detail', pk=pk)

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/profile.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

@login_required
def remove_from_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f"{product.name} removed from wishlist.")
    return redirect('wishlist')
