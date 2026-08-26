# Walkthrough: E-Commerce Site Implementation

We have built a full-featured e-commerce site using Django, SQLite, HTML, Vanilla CSS, and JavaScript.

---

## What Was Created

### 1. Backend & Architecture
- **Centralized Environment**: Installed `django` and verified `pillow` within `C:\Users\AAMIR SHAMSI\Agentic_Ai\.venv`.
- **Modular Django Structure**:
  - `core`: Django configuration directory ([settings.py](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/core/settings.py), [urls.py](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/core/urls.py)).
  - `shop`: Product catalog, categories, search, session-based cart, order placement, and Django Admin configurations ([models.py](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/shop/models.py), [views.py](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/shop/views.py), [urls.py](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/shop/urls.py), [cart.py](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/shop/cart.py)).
  - `accounts`: User authentication views for signup, login, and logout ([forms.py](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/accounts/forms.py), [views.py](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/accounts/views.py), [urls.py](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/accounts/urls.py)).

### 2. Database Models & Seeding
- Created `Category`, `Product`, `Order`, and `OrderItem` models with proper indexes and relationships.
- Ran migrations (`shop.0001_initial`, `auth`, `sessions`, `admin`).
- Created Django superuser credentials (`admin` / `admin123`).
- Ran [`seed_data.py`](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/seed_data.py) to automatically seed categories (*Electronics*, *Apparel*, *Home & Accessories*) and sample products.

### 3. Frontend & Aesthetics
- **Custom Dark Glassmorphic Design**: Built [`style.css`](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/shop/static/shop/css/style.css) featuring Outfit typography, slate dark mode background, gradient brand logo, hover card elevation, and emerald price badges.
- **Templates**:
  - [`base.html`](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/shop/templates/shop/base.html): Sticky navbar, search bar, live cart count badge, user state controls.
  - [`list.html`](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/shop/templates/shop/product/list.html): Category filter sidebar, product grid.
  - [`detail.html`](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/shop/templates/shop/product/detail.html): Image, stock badges, description, and add-to-cart form.
  - [`cart/detail.html`](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/shop/templates/shop/cart/detail.html): Interactive cart table with quantity selectors and subtotal calculations.
  - [`order/create.html`](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/shop/templates/shop/order/create.html) & [`order/created.html`](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/shop/templates/shop/order/created.html): Shipping details collection and confirmation view.
  - [`login.html`](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/accounts/templates/accounts/login.html) & [`register.html`](file:///c:/Users/AAMIR%20SHAMSI/Agentic_Ai/CodeAlpha/ecommerce_site/accounts/templates/accounts/register.html): Styled authentication cards.

---

## Verification Results

- **System Check**: Executed `..\..\.venv\Scripts\python.exe manage.py check` with output `System check identified no issues (0 silenced)`.
- **Database Seed**: Database successfully populated with sample items.

---

## How to Run the Server

To start the local development server:

```powershell
..\..\.venv\Scripts\python.exe manage.py runserver
```

Then open your browser at:
- **E-Commerce Home**: `http://127.0.0.1:8000/`
- **Django Admin Dashboard**: `http://127.0.0.1:8000/admin/` (Login with `admin` / `admin123`)
