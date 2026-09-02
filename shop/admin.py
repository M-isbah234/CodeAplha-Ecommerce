from django.contrib import admin
from django.db.models import Sum
from .models import Category, Product, ProductVariant, ProductImage, Order, OrderItem, Review, Wishlist

class LowStockFilter(admin.SimpleListFilter):
    title = 'Inventory Alert'
    parameter_name = 'stock_alert'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Low Stock (< 5)'),
            ('out', 'Out of Stock (0)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(stock__lt=5, stock__gt=0)
        if self.value() == 'out':
            return queryset.filter(stock=0)
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent']
    list_filter = ['parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created']
    list_filter = ['available', 'created', 'updated', 'category', LowStockFilter]
    list_editable = ['price', 'stock', 'available']
    search_fields = ['name', 'category__name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]
    date_hierarchy = 'created'


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'color', 'price_modifier', 'stock']
    list_filter = [LowStockFilter, 'size', 'color']
    list_editable = ['price_modifier', 'stock']
    search_fields = ['product__name', 'size', 'color']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product', 'variant']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'email', 'status', 'paid', 'created', 'order_total']
    list_filter = ['status', 'paid', 'created', 'updated']
    search_fields = ['first_name', 'last_name', 'email', 'id']
    list_editable = ['status', 'paid']
    inlines = [OrderItemInline]
    date_hierarchy = 'created'

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Customer'
    
    def order_total(self, obj):
        return obj.get_total_cost()
    order_total.short_description = 'Total (PKR)'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'text']
    readonly_fields = ['created_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']
    filter_horizontal = ['products']
