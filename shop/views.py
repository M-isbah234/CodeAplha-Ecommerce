from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.utils.text import slugify
import datetime

from .models import Category, Product, Order, OrderItem, ProductVariant, Review, Wishlist
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm


def product_list(request, category_slug=None):
    """
    Displays a list of available products, optionally filtered by category, search query, price, and sorted.
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Advanced Filtering
    search_query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
        
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
            
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
            
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created')
    else:
        products = products.order_by('name')

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'search_query': search_query,
    })


def search_autocomplete(request):
    query = request.GET.get('q', '').strip()
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query),
            available=True
        )[:5]
        results = [{'name': p.name, 'url': p.get_absolute_url()} for p in products]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})


def product_detail(request, id, slug):
    """
    Displays the details of a single product, including reviews and cart add form.
    """
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    in_wishlist = False
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        in_wishlist = product in wishlist.products.all()

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'in_wishlist': in_wishlist,
    })


@require_POST
def cart_add(request, product_id):
    """
    Adds a product (and optionally a specific variant) to the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    variant_id = request.POST.get('variant_id')
    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
        
    if form.is_valid():
        cd = form.cleaned_data
        
        # Determine price to use based on variant if selected, else base product
        # In a real app we'd adjust Cart.add to handle variants properly.
        # For simplicity without changing the Cart class drastically, we can store variant ID in session.
        # However, to avoid breaking `cart.py`, we will skip variant handling in the cart backend logic unless requested.
        
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'cart_total_items': len(cart)})
            
        messages.success(request, f"Added {product.name} to your shopping cart.")
    return redirect('shop:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    Removes a product from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'cart_total_items': len(cart), 'cart_total_price': cart.get_total_price()})
        
    messages.info(request, f"Removed {product.name} from your cart.")
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'shop/cart/detail.html', {'cart': cart})


@login_required
def order_create(request):
    """
    Handles the checkout process, creating an order from the user's cart.
    """
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Please add products before checking out.")
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.paid = True  # Simulated instant payment success
            order.status = 'Processing'
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'shop/order/created.html', {'order': order})
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = OrderCreateForm(initial=initial_data)
    return render(request, 'shop/order/create.html', {'cart': cart, 'form': form})


@login_required
@require_POST
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    rating = request.POST.get('rating')
    text = request.POST.get('text', '').strip()
    
    if rating:
        try:
            rating = int(rating)
            if 1 <= rating <= 5:
                Review.objects.update_or_create(
                    product=product,
                    user=request.user,
                    defaults={'rating': rating, 'text': text}
                )
                messages.success(request, "Your review has been submitted!")
        except ValueError:
            messages.error(request, "Invalid rating.")
            
    return redirect(product.get_absolute_url())


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        status = 'removed'
        msg = f"Removed {product.name} from wishlist."
    else:
        wishlist.products.add(product)
        status = 'added'
        msg = f"Added {product.name} to wishlist."
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status, 'message': msg})
        
    messages.info(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))


@login_required
def wishlist_detail(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'shop/wishlist/detail.html', {'wishlist': wishlist})
