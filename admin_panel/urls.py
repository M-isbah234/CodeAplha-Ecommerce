from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:id>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:id>/delete/', views.product_delete, name='product_delete'),
    
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:id>/', views.order_detail, name='order_detail'),
    
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
]
