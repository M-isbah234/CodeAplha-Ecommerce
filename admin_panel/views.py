from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
import datetime
from django.db.models import Sum

from shop.models import Product, Order, Category, ProductVariant, OrderItem
from .forms import ProductForm, CategoryForm

@staff_member_required
def dashboard(request):
    orders = Order.objects.all().order_by('-created')
    total_sales = sum(order.get_total_cost() for order in orders if order.paid)
    active_orders_count = orders.filter(paid=True, status__in=['Pending', 'Processing', 'Shipped']).count()
    
    monthly_expenses = 100.00 + float(total_sales) * 0.15
    net_profit = float(total_sales) - monthly_expenses
    
    low_stock_products = Product.objects.filter(stock__lt=5)
    low_stock_variants = ProductVariant.objects.filter(stock__lt=5)

    chart_data = []
    today = datetime.date.today()
    for i in range(6, -1, -1):
        day = today - datetime.timedelta(days=i)
        day_orders = orders.filter(created__date=day, paid=True)
        day_sales = float(sum(order.get_total_cost() for order in day_orders))
        day_expenses = 10.00 + day_sales * 0.10 if day_sales > 0 else 5.00
        chart_data.append({
            'day': day.strftime('%a'),
            'sales': day_sales,
            'expenses': day_expenses,
            'sales_pct': min(100, int(day_sales / 500.0 * 100)) if day_sales > 0 else 2,
            'expenses_pct': min(100, int(day_expenses / 500.0 * 100)) if day_expenses > 0 else 2,
        })

    return render(request, 'admin_panel/dashboard.html', {
        'orders': orders[:10],
        'total_sales': total_sales,
        'active_orders_count': active_orders_count,
        'monthly_expenses': monthly_expenses,
        'net_profit': net_profit,
        'chart_data': chart_data,
        'low_stock_products': low_stock_products,
        'low_stock_variants': low_stock_variants,
    })


@staff_member_required
def product_list(request):
    products = Product.objects.all().order_by('-created')
    return render(request, 'admin_panel/product_list.html', {'products': products})

@staff_member_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' created.")
            return redirect('admin_panel:product_list')
    else:
        form = ProductForm()
    return render(request, 'admin_panel/product_form.html', {'form': form, 'is_edit': False})

@staff_member_required
def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated.")
            return redirect('admin_panel:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_panel/product_form.html', {'form': form, 'is_edit': True, 'product': product})

@staff_member_required
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' deleted.")
        return redirect('admin_panel:product_list')
    return render(request, 'admin_panel/confirm_delete.html', {'object': product})

@staff_member_required
def order_list(request):
    orders = Order.objects.all().order_by('-created')
    return render(request, 'admin_panel/order_list.html', {'orders': orders})

@staff_member_required
def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {status}.")
            return redirect('admin_panel:order_detail', id=order.id)
    return render(request, 'admin_panel/order_detail.html', {'order': order})

@staff_member_required
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'admin_panel/category_list.html', {'categories': categories})

@staff_member_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"Category '{cat.name}' created.")
            return redirect('admin_panel:category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin_panel/category_form.html', {'form': form})

from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, Avg, F

@staff_member_required
def analytics_view(request):
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)
    
    # 30-day stats
    thirty_day_orders = Order.objects.filter(created__gte=thirty_days_ago, paid=True)
    thirty_day_sales = sum(order.get_total_cost() for order in thirty_day_orders)
    thirty_day_aov = thirty_day_sales / thirty_day_orders.count() if thirty_day_orders.count() > 0 else 0
    thirty_day_profit = thirty_day_sales * 0.20 # 20% margin assumption
    
    # 7-day stats
    seven_day_orders = Order.objects.filter(created__gte=seven_days_ago, paid=True)
    seven_day_sales = sum(order.get_total_cost() for order in seven_day_orders)
    seven_day_aov = seven_day_sales / seven_day_orders.count() if seven_day_orders.count() > 0 else 0
    seven_day_profit = seven_day_sales * 0.20 # 20% margin assumption
    
    # Top selling SKUs
    top_selling_skus = OrderItem.objects.filter(order__paid=True).values('product__name').annotate(total_qty=Sum('quantity')).order_by('-total_qty')[:5]
    
    # Fastest moving categories
    fastest_categories = OrderItem.objects.filter(order__paid=True).values('product__category__name').annotate(total_qty=Sum('quantity')).order_by('-total_qty')[:5]
    
    # Dead stock
    dead_stock = Product.objects.annotate(sold=Sum('order_items__quantity')).filter(sold__isnull=True).order_by('-stock')[:5]
    
    context = {
        'thirty_day_sales': thirty_day_sales,
        'thirty_day_aov': thirty_day_aov,
        'thirty_day_profit': thirty_day_profit,
        'seven_day_sales': seven_day_sales,
        'seven_day_aov': seven_day_aov,
        'seven_day_profit': seven_day_profit,
        'top_selling_skus': top_selling_skus,
        'fastest_categories': fastest_categories,
        'dead_stock': dead_stock,
    }
    return render(request, 'admin_panel/analytics.html', context)

@staff_member_required
def settings_view(request):
    return render(request, 'admin_panel/settings.html')