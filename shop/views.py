from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    search_query = request.GET.get('q', '').strip()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'search_query': search_query,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
    })


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
        messages.success(request, f"Added {product.name} to your shopping cart.")
    return redirect('shop:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
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
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Clear cart session
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


from django.utils.text import slugify

@login_required
def admin_dashboard(request):
    # Fetch all orders to calculate KPI
    orders = Order.objects.all().order_by('-created')
    total_sales = sum(order.get_total_cost() for order in orders)
    active_orders_count = orders.filter(paid=True).count()
    
    # Simulating expenses (e.g. fixed warehouse/operations + dynamic shipping)
    monthly_expenses = 100.00 + float(total_sales) * 0.15
    net_profit = float(total_sales) - monthly_expenses
    
    # Form processing for quick add product
    categories = Category.objects.all()
    if request.method == 'POST' and 'quick_add_product' in request.POST:
        name = request.POST.get('name')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        
        if name and price and category_id:
            category = get_object_or_404(Category, id=category_id)
            slug = slugify(name)
            
            # Simple check to avoid duplicate slug crash
            base_slug = slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                
            product = Product.objects.create(
                category=category,
                name=name,
                slug=slug,
                price=price,
                stock=50, # default stock
                image=image,
                available=True
            )
            messages.success(request, f"Product '{product.name}' was published successfully!")
            return redirect('shop:admin_dashboard')
        else:
            messages.error(request, "Please fill out all product details.")

    # Simulated last 7 days sales vs expenses for chart
    import datetime
    chart_data = []
    today = datetime.date.today()
    for i in range(6, -1, -1):
        day = today - datetime.timedelta(days=i)
        # Calculate daily sales from orders placed on this day
        day_orders = orders.filter(created__date=day)
        day_sales = float(sum(order.get_total_cost() for order in day_orders))
        # Simulated expense for that day
        day_expenses = 10.00 + day_sales * 0.10 if day_sales > 0 else 5.00
        chart_data.append({
            'day': day.strftime('%a'),
            'sales': day_sales,
            'expenses': day_expenses,
            'sales_pct': min(100, int(day_sales / 500.0 * 100)) if day_sales > 0 else 2,
            'expenses_pct': min(100, int(day_expenses / 500.0 * 100)) if day_expenses > 0 else 2,
        })

    return render(request, 'shop/dashboard.html', {
        'orders': orders[:8], # Show recent 8 orders
        'total_sales': total_sales,
        'active_orders_count': active_orders_count,
        'monthly_expenses': monthly_expenses,
        'net_profit': net_profit,
        'categories': categories,
        'chart_data': chart_data,
    })
