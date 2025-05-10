from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category
from orders.models import Order, OrderItem

def home(request):
    """
    Home page view with featured products
    """
    products = Product.objects.filter(available=True)[:8]  # Show 8 products
    categories = Category.objects.all()
    
    context = {
        'title': "Closure's Online Supermarket",
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

def product_list(request):
    """
    View for listing all products with filtering
    """
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Paging
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Product Catalog',
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_id,
        'search_query': search_query,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, product_id):
    """
    View for product details
    """
    product = get_object_or_404(Product, id=product_id, available=True)
    
    recommended_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'title': product.name,
        'product': product,
        'recommended_products': recommended_products,
    }
    return render(request, 'store/product_detail.html', context)

def is_staff_or_admin(user):
    """Helper function to check if user is staff or admin"""
    return user.is_staff or user.role in [user.STAFF, user.ADMIN]

@user_passes_test(is_staff_or_admin)
def admin_dashboard(request):
    # Get statistics
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status=Order.PENDING).count()
    low_stock_products = Product.objects.filter(stock_quantity__lt=10).count()
    
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    context = {
        'title': 'Admin Dashboard',
        'total_products': total_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
    }
    return render(request, 'store/admin/dashboard.html', context)

@user_passes_test(is_staff_or_admin)
def inventory_management(request):
    products = Product.objects.all().order_by('category', 'name')
    
    # Add paging
    paginator = Paginator(products, 20)  # 20 products per page
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)
    
    context = {
        'title': 'Inventory Management',
        'products': products_page,
    }
    return render(request, 'store/admin/inventory.html', context)

@user_passes_test(is_staff_or_admin)
def order_management(request):
    """
    Order management
    """
    orders = Order.objects.all().order_by('-created_at')
    
    # Filter 
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    # Add page per 20 orders
    paginator = Paginator(orders, 20)  # 20 orders per page
    page_number = request.GET.get('page')
    orders_page = paginator.get_page(page_number)
    
    context = {
        'title': 'Order Management',
        'orders': orders_page,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status,
    }
    return render(request, 'store/admin/orders.html', context)

@user_passes_test(is_staff_or_admin)
def update_order_status(request, order_id):
    """
    Update order status
    """
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {order.get_status_display()}.")
        else:
            messages.error(request, "Invalid status.")
    
    return redirect('order_management')
