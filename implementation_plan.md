# Implementation Plan: E-Commerce Site

<!-- ..\..\.venv\Scripts\python.exe manage.py runserver -->

This document outlines the detailed implementation plan to build a responsive, premium e-commerce site with product listings, product details, a shopping cart, checkout/order processing, and user registration/login.

We will use Django (Python) for the backend, SQLite for the database, and standard HTML, Vanilla CSS, and JavaScript for the frontend.

---

## Technical Stack & Packages

We will use the following Python packages:
- **`Django`**: Core web framework.
- **`Pillow`**: Python Imaging Library to process product image uploads (already installed in the environment).

We will use the existing virtual environment in the parent folder `..\..\.venv` (`C:\Users\AAMIR SHAMSI\Agentic_Ai\.venv`) to keep all dependencies centralized as requested.

---

## Proposed Folder Structure

To keep the project clean, organized, and properly separated, we will structure it as follows:

```
ecommerce_site/
│
├── manage.py                      # Django management script
│
├── core/                          # Project configuration directory
│   ├── __init__.py
│   ├── settings.py                # Main settings (configured for static files, media, apps)
│   ├── urls.py                    # Root URL routing (includes shop and accounts)
│   └── wsgi.py / asgi.py
│
├── shop/                          # Main shop application (products, cart, orders)
│   ├── migrations/
│   ├── templates/
│   │   └── shop/
│   │       ├── base.html          # Base layout with navbar, footer, and styling links
│   │       ├── index.html         # Homepage (product listings, category search)
│   │       ├── product_detail.html# Product detail page with image and add-to-cart
│   │       ├── cart.html          # Shopping cart overview (update quantities, remove items)
│   │       ├── checkout.html      # Shipping info and order placement
│   │       └── order_success.html # Order confirmation message
│   ├── static/
│   │   └── shop/
│   │       ├── css/
│   │       │   └── style.css      # Premium custom CSS (vibrant palette, glassmorphism, animations)
│   │       └── js/
│   │           └── main.js        # Client-side interactivity (AJAX cart updates, animations)
│   ├── __init__.py
│   ├── admin.py                   # Register models for Django admin dashboard
│   ├── apps.py
│   ├── models.py                  # Core models: Category, Product, Order, OrderItem
│   ├── urls.py                    # URL routing for the shop app
│   └── views.py                   # View logic (product list, product detail, cart functions, checkout)
│
├── accounts/                      # Authentication application
│   ├── migrations/
│   ├── templates/
│   │   └── accounts/
│   │       ├── login.html         # Elegant Login form
│   │       └── register.html      # Clean Signup form
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py                    # URL routing for auth views
│   └── views.py                   # View logic (login, register, logout)
│
├── media/                         # Uploaded product images
└── requirements.txt               # Dependencies list
```

---

## Database Schema (SQLite)

We will use Django's ORM to define the database schema. The main tables will be:

1. **`User`** (Django Built-in Auth User):
   - Handles standard authentication (Username, Email, Password, First/Last Name).

2. **`Category`**:
   - `name`: CharField (e.g., "Electronics", "Apparel")
   - `slug`: SlugField (unique identifier for URLs)

3. **`Product`**:
   - `category`: ForeignKey to `Category`
   - `name`: CharField
   - `slug`: SlugField (unique identifier)
   - `image`: ImageField (uploaded to `products/`)
   - `description`: TextField
   - `price`: DecimalField (e.g., max_digits=10, decimal_places=2)
   - `stock`: PositiveIntegerField
   - `available`: BooleanField
   - `created`: DateTimeField
   - `updated`: DateTimeField

4. **`Order`**:
   - `user`: ForeignKey to `User` (nullable for guest checkout, but we will restrict checkout to registered/logged-in users as requested)
   - `first_name`, `last_name`: CharField
   - `email`: EmailField
   - `address`, `city`, `postal_code`, `country`: CharField
   - `created`: DateTimeField
   - `updated`: DateTimeField
   - `paid`: BooleanField (defaults to False; can mark True upon order completion)
   - `total_cost`: DecimalField

5. **`OrderItem`**:
   - `order`: ForeignKey to `Order`
   - `product`: ForeignKey to `Product`
   - `price`: DecimalField
   - `quantity`: PositiveIntegerField

> [!NOTE]
> For the **Shopping Cart**, we will implement a clean, lightweight session-based cart. This is standard in Django and avoids bloating the database with incomplete/abandoned carts, keeping database storage clean and efficient.

---

## Step-by-Step Implementation Strategy

### Phase 1: Initialize Project & Core Configuration
1. Install Django in the existing virtual environment `..\..\.venv` (`C:\Users\AAMIR SHAMSI\Agentic_Ai\..venv`).
2. Generate requirements.txt.
3. Start the project `core` and create apps `shop` and `accounts`.
4. Configure `core/settings.py` for Database, Media uploads, and static assets.
5. Setup main URLs to route to the apps.

### Phase 2: Define Models & Django Admin
1. Create `Category`, `Product`, `Order`, and `OrderItem` models in `shop/models.py`.
2. Generate migrations and run `migrate` to initialize database tables.
3. Register the models in `shop/admin.py` and create a superuser for managing products via the Django admin interface.

### Phase 3: Setup Session-Based Shopping Cart
1. Create a `cart.py` utility class in the `shop` directory.
2. Initialize, add, update, remove, and query items in the cart using `request.session`.
3. Build context processors to expose the cart items and total count to all templates (for the header badge).

### Phase 4: Build Authentication (Accounts App)
1. Build register, login, and logout views.
2. Create visually stunning login/register forms using CSS grids and floating labels.
3. Set up redirects so checkout pages are restricted to authenticated users.

### Phase 5: Develop Shop Views and Front-End Pages
1. **Homepage / Products Listing**: Grid system displaying products, with category filters and sidebar/navbar search.
2. **Product Details Page**: Clean page with item images, stock status, descriptions, and a smooth "Add to Cart" button.
3. **Cart Overview**: Visual list of items with dynamically adjustable quantities (using JavaScript / AJAX, or clean POST forms), individual totals, and total price display.
4. **Checkout Form**: Details page for delivery information, calculated order summaries, and a checkout submission.
5. **Success Confirmation**: Screen demonstrating order success with order details.

### Phase 6: Styling & Micro-interactions (CSS & JavaScript)
- Design a custom vanilla CSS stylesheet (`style.css`) using:
  - Sleek dark/light dynamic theme colors (deep slate, premium violet accents, gold highlights).
  - Modern fonts (Outfit / Inter).
  - Glassmorphic panels with subtle drop shadows.
  - Hover micro-animations on product cards, cart badges, and form buttons.
- Create client-side JS (`main.js`) for:
  - Dynamic quantity updating.
  - Interactive alerts and toasts.
  - Cart counter animations.

---

## Verification Plan

### Automated Tests
- Run `python manage.py check` to verify configuration validity.
- Run `python manage.py test` to ensure Django builds and registers apps correctly.

### Manual Verification
1. Open the dev server on `http://127.0.0.1:8000/`.
2. Register a new user, log in, and log out.
3. Access `/admin` to seed sample products and categories.
4. Add items to the cart, edit quantities, and verify calculations.
5. Navigate to checkout, fill shipping details, and place an order.
6. Verify database records for the placed order inside Django Admin.
