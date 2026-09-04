import os
import django
import shutil
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from shop.models import Category, Product, ProductVariant, Review, ProductImage, Order, OrderItem
from django.contrib.auth.models import User

# Delete existing data to start fresh
print("Deleting existing products, categories, variants, reviews, and orders...")
OrderItem.objects.all().delete()
Order.objects.all().delete()
ProductVariant.objects.all().delete()
Review.objects.all().delete()
ProductImage.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()

# Create Admin User if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Created superuser 'admin' with password 'admin'")
admin_user = User.objects.get(username='admin')

# Create a couple dummy customers
customer1, _ = User.objects.get_or_create(username='customer1', defaults={'email': 'c1@test.com'})
customer2, _ = User.objects.get_or_create(username='customer2', defaults={'email': 'c2@test.com'})

# Create Categories
print("Creating categories...")

# Parent Categories
apparel = Category.objects.create(name='Apparel', slug='apparel')
electronics = Category.objects.create(name='Electronics', slug='electronics')
home = Category.objects.create(name='Home & Living', slug='home-living')
fitness = Category.objects.create(name='Fitness & Sports', slug='fitness')
beauty = Category.objects.create(name='Beauty & Health', slug='beauty')

# Subcategories
Category.objects.create(name='T-Shirts', slug='t-shirts', parent=apparel)
Category.objects.create(name='Hoodies', slug='hoodies', parent=apparel)
Category.objects.create(name='Sneakers', slug='sneakers', parent=apparel)

Category.objects.create(name='Smartphones', slug='smartphones', parent=electronics)
Category.objects.create(name='Laptops', slug='laptops', parent=electronics)
Category.objects.create(name='Audio', slug='audio', parent=electronics)

Category.objects.create(name='Furniture', slug='furniture', parent=home)
Category.objects.create(name='Decor', slug='decor', parent=home)

Category.objects.create(name='Supplements', slug='supplements', parent=fitness)
Category.objects.create(name='Gym Gear', slug='gym-gear', parent=fitness)

Category.objects.create(name='Skincare', slug='skincare', parent=beauty)
Category.objects.create(name='Fragrances', slug='fragrances', parent=beauty)

print("Categories seeded successfully!")

# Seed products (Generate 20 dummy products)
print("Seeding products, variants, and reviews...")
products = []
categories = list(Category.objects.filter(parent__isnull=False))

for i in range(1, 25):
    cat = random.choice(categories)
    price = round(random.uniform(10.0, 300.0), 2)
    stock = random.randint(2, 50)
    
    p = Product.objects.create(
        category=cat,
        name=f"Premium {cat.name[:-1]} {i}",
        slug=f"premium-{cat.slug}-{i}",
        description=f"This is a high-quality {cat.name[:-1].lower()} perfect for everyday use. Designed with modern aesthetics and premium materials.",
        price=price,
        stock=stock,
        available=True
    )
    products.append(p)
    
    # Add variants for apparel
    if cat.parent == apparel:
        ProductVariant.objects.create(product=p, size='S', color='Black', stock=random.randint(0, 10))
        ProductVariant.objects.create(product=p, size='M', color='Black', stock=random.randint(5, 20))
        ProductVariant.objects.create(product=p, size='L', color='White', stock=random.randint(1, 15))
        
    # Add reviews
    num_reviews = random.randint(0, 3)
    for _ in range(num_reviews):
        user = random.choice([admin_user, customer1, customer2])
        Review.objects.update_or_create(
            product=p,
            user=user,
            defaults={
                'rating': random.randint(3, 5),
                'text': "Really great product, exceeded my expectations."
            }
        )

# Seed some Orders
print("Seeding dummy orders...")
statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
for i in range(15):
    user = random.choice([customer1, customer2])
    order = Order.objects.create(
        user=user,
        first_name=user.username,
        last_name="Test",
        email=user.email,
        address="123 Dummy St",
        postal_code="12345",
        city="Testville",
        paid=True,
        status=random.choice(statuses)
    )
    # Give order a random date within last 7 days
    order.created = datetime.now() - timedelta(days=random.randint(0, 6))
    order.save()
    
    # Add items to order
    num_items = random.randint(1, 4)
    for _ in range(num_items):
        prod = random.choice(products)
        OrderItem.objects.create(
            order=order,
            product=prod,
            price=prod.price,
            quantity=random.randint(1, 3)
        )

print("Seeding completed successfully! 24 Products, 12 Subcategories, 15 Orders generated.")
