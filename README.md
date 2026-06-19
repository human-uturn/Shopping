# Django Online Shopping Application

A complete e-commerce web application built with Django framework and Python, featuring product management, shopping cart, and PDF order generation.

## Features

### Admin Features
- **Product Management**: Create and manage products through Django admin interface
- **Auto-generated Product Numbers**: Each product gets a unique product number automatically
- **Image Upload**: Support for JPEG, PNG, and GIF image formats
- **Product Fields**: Product number, name, description, category, quantity, price, and picture

### User Features
- **Product Search**: Search products by name or category
- **Product Browsing**: View all available products with images
- **Product Details**: View detailed information about each product
- **Shopping Cart**: Add products to cart, update quantities, and remove items
- **Cart Summary**: View total items and total amount in cart
- **Checkout**: Place orders or cancel cart
- **Order PDF**: Generate and download PDF documents for completed orders

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd Shopping
   ```

2. **Create and activate virtual environment** (if not already done)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - User interface: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Usage

### Admin Interface

1. Log in to the admin panel at `/admin/`
2. Navigate to "Products" section
3. Click "Add Product" to create a new product
4. Fill in the product details:
   - Product name
   - Short description (one line)
   - Category
   - Quantity (available stock)
   - Price
   - Product picture (JPEG, PNG, or GIF)
5. The product number will be auto-generated when you save
6. Products can be searched and filtered in the admin interface

### User Interface

1. **Browse Products**: View all available products on the home page
2. **Search Products**: Use the search bar to find products by name or category
3. **View Product Details**: Click on any product to see full details
4. **Add to Cart**: Click "Add to Cart" button on product detail page
5. **View Cart**: Click the cart icon in the navigation bar
6. **Update Cart**: Change quantities or remove items from cart
7. **Checkout**: Click "Proceed to Checkout" to review and place order
8. **Place Order**: Confirm order or cancel
9. **Download PDF**: After placing order, download the order confirmation PDF

## Project Structure

```
Shopping/
├── manage.py
├── requirements.txt
├── README.md
├── shopping_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/
│   ├── models.py          # Product and Order models
│   ├── admin.py           # Admin configuration
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   ├── forms.py           # Form classes
│   ├── utils.py           # PDF generation utility
│   └── templates/
│       └── shop/
│           ├── base.html
│           ├── product_list.html
│           ├── product_detail.html
│           ├── cart.html
│           ├── checkout.html
│           └── order_success.html
├── media/                 # User uploaded files (product images)
└── db.sqlite3            # SQLite database
```

## Database

The application uses SQLite database (Django's default). The database file `db.sqlite3` will be created automatically when you run migrations.

## Technologies Used

- **Django 5.2.8**: Web framework
- **Python 3**: Programming language
- **SQLite**: Database
- **ReportLab**: PDF generation
- **Pillow**: Image processing
- **Bootstrap 5**: Frontend framework

## Notes

- Product images are stored in the `media/products/` directory
- Shopping cart is session-based (cleared when browser session ends)
- Product quantities are automatically reduced when orders are placed
- Order PDFs include order number, date, product list, and total amount

