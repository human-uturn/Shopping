from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from .models import Product, Order
from .forms import ProductSearchForm
from .utils import generate_order_pdf
import json


def product_list(request):
    """Display  product list with search functionality"""
    form = ProductSearchForm(request.GET)
    products = Product.objects.filter(quantity__gt=0)
    
    if form.is_valid():
        query = form.cleaned_data.get('query', '')
        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(category__icontains=query)
            )
    
    # Get cart count for display
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    
    context = {
        'products': products,
        'form': form,
        'cart_count': cart_count,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    """Display product details"""
    product = get_object_or_404(Product, pk=pk)
    
    # Get cart count for display
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    
    context = {
        'product': product,
        'cart_count': cart_count,
    }
    return render(request, 'shop/product_detail.html', context)


def add_to_cart(request, pk):
    """Add product to cart"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(product.id)
        
        if product_id in cart:
            # Increase quantity if already in cart
            cart[product_id]['quantity'] += 1
        else:
            # Add new item to cart
            cart[product_id] = {
                'product_id': product.id,
                'product_number': product.product_number,
                'name': product.name,
                'price': str(product.price),
                'quantity': 1,
                'picture': product.picture.url if product.picture else '',
            }
        
        request.session['cart'] = cart
        request.session.modified = True
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cart_count = sum(item['quantity'] for item in cart.values())
            return JsonResponse({'success': True, 'cart_count': cart_count})
        
        return redirect('cart')
    
    return redirect('product_detail', pk=pk)


def remove_from_cart(request, pk):
    """Remove product from cart"""
    cart = request.session.get('cart', {})
    product_id = str(pk)
    
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('cart')


def update_cart(request, pk):
    """Update product quantity in cart"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(pk)
        quantity = int(request.POST.get('quantity', 1))
        
        if product_id in cart and quantity > 0:
            cart[product_id]['quantity'] = quantity
            request.session['cart'] = cart
            request.session.modified = True
        elif quantity <= 0:
            # Remove if quantity is 0 or less
            if product_id in cart:
                del cart[product_id]
                request.session['cart'] = cart
                request.session.modified = True
    
    return redirect('cart')


def cart(request):
    """Display shopping cart"""
    cart = request.session.get('cart', {})
    cart_items = []
    total_amount = 0
    total_items = 0
    
    for item in cart.values():
        quantity = item['quantity']
        price = float(item['price'])
        subtotal = quantity * price
        item['subtotal'] = subtotal
        cart_items.append(item)
        total_amount += subtotal
        total_items += quantity
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'total_items': total_items,
        'cart_count': total_items,
    }
    return render(request, 'shop/cart.html', context)


def checkout(request):
    """Checkout and create order"""
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('product_list')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'order':
            # Calculate total
            total_amount = sum(
                float(item['price']) * item['quantity']
                for item in cart.values()
            )
            
            # Create order
            order = Order.objects.create(
                total_amount=total_amount,
                items=cart
            )
            
            # Update product quantities
            for item in cart.values():
                product = Product.objects.get(id=item['product_id'])
                product.quantity -= item['quantity']
                product.save()
            
            # Clear cart
            request.session['cart'] = {}
            request.session.modified = True
            
            return redirect('order_success', order_id=order.id)
        
        elif action == 'cancel':
            # Clear cart
            request.session['cart'] = {}
            request.session.modified = True
            return redirect('product_list')
    
    # Display checkout page
    cart_items = []
    total_amount = 0
    total_items = 0
    
    for item in cart.values():
        quantity = item['quantity']
        price = float(item['price'])
        subtotal = quantity * price
        item['subtotal'] = subtotal
        cart_items.append(item)
        total_amount += subtotal
        total_items += quantity
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'total_items': total_items,
    }
    return render(request, 'shop/checkout.html', context)


def order_success(request, order_id):
    """Display order success page"""
    order = get_object_or_404(Order, pk=order_id)
    
    context = {
        'order': order,
    }
    return render(request, 'shop/order_success.html', context)


def download_order_pdf(request, order_id):
    """Generate and download order PDF"""
    order = get_object_or_404(Order, pk=order_id)
    
    # Generate PDF
    pdf_buffer = generate_order_pdf(order)
    
    # Create HTTP response with PDF
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order.order_number}.pdf"'
    
    return response
