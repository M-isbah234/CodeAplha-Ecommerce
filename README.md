# 🛒 Premium E-Commerce Site

A professional, responsive e-commerce platform built with Django. This project provides a complete shopping experience including product browsing, category-based filtering, a shopping cart system, and a secure checkout process.

## 🚀 Features

- **Product Catalog:** Browse products with detailed descriptions, pricing, and images.
- **Category Management:** Organized product hierarchy with support for parent and child categories.
- **Shopping Cart:** Add, remove, and update product quantities in a session-based cart.
- **Search Functionality:** Quick search for products by name or description.
- **User Authentication:** Secure user registration and login system.
- **Order Processing:** Complete checkout flow from shipping details to order confirmation.
- **Responsive Design:** A modern, premium UI designed to work across all device sizes.

## 🛠️ Tech Stack

- **Backend:** Python 3.x, Django
- **Database:** SQLite (Development)
- **Frontend:** HTML5, CSS3 (Custom Premium Styling), Vanilla JavaScript
- **Image Processing:** Pillow

## ⚙️ Getting Started

### Prerequisites
Ensure you have Python installed on your system.

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ecommerce_site
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   # Activate on Windows:
   .\venv\Scripts\activate
   # Activate on macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

### Running the Application

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the site:**
   Open your browser and navigate to `http://127.0.0.1:8000/`

3. **Admin Panel:**
   Access the Django admin dashboard at `http://127.0.0.1:8000/admin/` to manage products and categories.

4. **Control Panel:**
   Access the control panel at `http://127.0.0.1:8000/control-panel/` to manage products and categories.
## 📁 Project Structure

- `core/`: Project configuration and settings.
- `shop/`: Core e-commerce logic (products, cart, orders).
- `accounts/`: User authentication and profile management.
- `static/`: CSS, JavaScript, and other frontend assets.
- `media/`: User-uploaded product images.

## Production Warning: When you deploy to Vercel, remember that Vercel's file system is read-only. This means images uploaded through the admin panel will disappear after a few minutes.
## Solution: For production, you will eventually need to connect an external storage service like Cloudinary or AWS S3 (which is very common for Django apps). For now, during local development, it will work perfectly using your local media folder.