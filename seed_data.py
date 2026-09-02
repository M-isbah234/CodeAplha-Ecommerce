import os
import django
import shutil
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from shop.models import Category, Product, ProductVariant, Review, ProductImage
from django.contrib.auth.models import User

# Delete existing data to start fresh
print("Deleting existing products, categories, variants, and reviews...")
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

# Create Categories
print("Creating categories...")

# Parent Categories
apparel = Category.objects.create(name='Apparel', slug='apparel')
electronics = Category.objects.create(name='Electronics', slug='electronics')
home_accessories = Category.objects.create(name='Home & Accessories', slug='home-accessories')
fitness_gear = Category.objects.create(name='Fitness Gear', slug='fitness-gear')
nutrition_hub = Category.objects.create(name='Nutrition Hub', slug='nutrition-hub')
new_arrivals = Category.objects.create(name='New Arrivals', slug='new-arrivals')
best_sellers = Category.objects.create(name='Best Sellers', slug='best-sellers')

# Subcategories
graphic_tees = Category.objects.create(name='Graphic Tees', slug='graphic-tees', parent=apparel)
hoodies = Category.objects.create(name='Hoodies', slug='hoodies', parent=apparel)
activewear = Category.objects.create(name='Activewear', slug='activewear', parent=apparel)

smart_devices = Category.objects.create(name='Smart Devices', slug='smart-devices', parent=electronics)
gadgets = Category.objects.create(name='Gadgets', slug='gadgets', parent=electronics)

print("Categories seeded successfully!")

# Setup image directories
today = datetime.now()
relative_upload_path = f"products/{today.strftime('%Y/%m/%d')}"
target_media_dir = os.path.join("media", "products", today.strftime("%Y"), today.strftime("%m"), today.strftime("%d"))
os.makedirs(target_media_dir, exist_ok=True)

src_products_dir = os.path.join("media", "products")

product_images = {
    "indigo_katana_graphic_tee.jpg": "indigo_katana_graphic_tee.jpg",
    "vanilla_almond_mass_gainer.jpg": "vanilla_almond_mass_gainer.jpg",
    "aesthetic_minimalist_hoodie.jpg": "aesthetic_minimalist_hoodie.jpg",
    "performance_lifting_straps.jpg": "performance_lifting_straps.jpg",
    "sonicwave_wireless_earbuds.jpg": "sonicwave_wireless_earbuds.jpg",
    "apex_duffel_gym_bag.jpg": "apex_duffel_gym_bag.jpg",
}

for img_name in product_images.keys():
    src_file = os.path.join(src_products_dir, img_name)
    dst_file = os.path.join(target_media_dir, img_name)
    if os.path.exists(src_file) and not os.path.exists(dst_file):
        shutil.copy(src_file, dst_file)

# Seed products
products_data = [
    {
        'category': graphic_tees,
        'name': 'Indigo Katana Graphic Tee',
        'slug': 'indigo-katana-graphic-tee',
        'description': 'A high-quality blue graphic t-shirt featuring a katana design and Japanese calligraphy. Designed for a comfortable fit and modern look.',
        'price': 45.00,
        'stock': 15,
        'image': f"{relative_upload_path}/indigo_katana_graphic_tee.jpg",
        'available': True,
    },
    {
        'category': nutrition_hub,
        'name': 'Vanilla Almond Mass Gainer',
        'slug': 'vanilla-almond-mass-gainer',
        'description': 'A large, premium protein powder supplement jar. Formulated with vanilla almond flavor to support high-performance training.',
        'price': 59.99,
        'stock': 8,
        'image': f"{relative_upload_path}/vanilla_almond_mass_gainer.jpg",
        'available': True,
    },
    {
        'category': hoodies,
        'name': 'Aesthetic Minimalist Hoodie',
        'slug': 'aesthetic-minimalist-hoodie',
        'description': 'A comfortable black minimalist hoodie made with organic materials. Offers a modern, clean, relaxed silhouette.',
        'price': 79.99,
        'stock': 3, # Low stock
        'image': f"{relative_upload_path}/aesthetic_minimalist_hoodie.jpg",
        'available': True,
    },
    {
        'category': fitness_gear,
        'name': 'Performance Lifting Straps (Pair)',
        'slug': 'performance-lifting-straps-pair',
        'description': 'Heavy-duty dark leather weightlifting straps providing superior grip and stability during heavy pulls.',
        'price': 34.00,
        'stock': 25,
        'image': f"{relative_upload_path}/performance_lifting_straps.jpg",
        'available': True,
    },
    {
        'category': gadgets,
        'name': 'SonicWave Wireless Earbuds Pro',
        'slug': 'sonicwave-wireless-earbuds-pro',
        'description': 'Black high-performance wireless earbuds with active noise cancellation, smart touch controls, and compact charging case.',
        'price': 149.00,
        'stock': 20,
        'image': f"{relative_upload_path}/sonicwave_wireless_earbuds.jpg",
        'available': True,
    },
    {
        'category': fitness_gear,
        'name': 'Apex Duffel Gym Bag',
        'slug': 'apex-duffel-gym-bag',
        'description': 'A premium canvas and leather duffel bag designed for gym wear and long weekend travels.',
        'price': 85.00,
        'stock': 10,
        'image': f"{relative_upload_path}/apex_duffel_gym_bag.jpg",
        'available': True,
    },
]

print("Seeding products, variants, and reviews...")
for prod_data in products_data:
    p = Product.objects.create(**prod_data)
    
    # Add some variants
    if p.slug == 'indigo-katana-graphic-tee':
        ProductVariant.objects.create(product=p, size='M', color='Blue', stock=10)
        ProductVariant.objects.create(product=p, size='L', color='Blue', stock=2) # Low stock alert trigger
    elif p.slug == 'aesthetic-minimalist-hoodie':
        ProductVariant.objects.create(product=p, size='S', color='Black', stock=5)
        ProductVariant.objects.create(product=p, size='L', color='Black', stock=12)
        
    # Add dummy reviews
    Review.objects.create(
        product=p,
        user=admin_user,
        rating=5 if p.price > 50 else 4,
        text="Great quality and fast shipping. Highly recommend this product!"
    )

print("Seeding completed successfully!")
