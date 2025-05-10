from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm

@login_required
def cart_detail(request):
    """
    Cart details
    """
    # Create user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    context = {
        'title': 'Your Shopping Cart',
        'cart': cart,
    }
    return render(request, 'orders/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    """
    Basically adding products to cart
    """
    product = get_object_or_404(Product, id=product_id, available=True)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock_quantity:
        messages.error(request, f"Sorry, only {product.stock_quantity} items available in stock.")
        return redirect('product_detail', product_id=product.id)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart.add_item(product, quantity)
    
    messages.success(request, f"Added {quantity} x {product.name} to your cart.")
    return redirect('cart_detail')

@login_required
def update_cart(request, item_id):
    """
    Update carts yadda yadda
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > cart_item.product.stock_quantity:
        messages.error(request, f"Sorry, only {cart_item.product.stock_quantity} items available in stock.")
    elif quantity <= 0:
        cart_item.delete()
        messages.success(request, f"Removed {cart_item.product.name} from your cart.")
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated successfully.")
    
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    """
    Remove
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    
    messages.success(request, f"Removed {cart_item.product.name} from your cart.")
    return redirect('cart_detail')

@login_required
def checkout(request):
    """
    Checkout process I think
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if cart.items.count() == 0:
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order(
                user=request.user,
                shipping_address=form.cleaned_data['shipping_address'],
                phone=form.cleaned_data['phone'],
            )
            order.save()
            
            for item in cart.items.all():
                # Delete the created order
                if item.quantity > item.product.stock_quantity:
                    messages.error(request, f"Sorry, only {item.product.stock_quantity} of {item.product.name} available in stock.")
                    order.delete()
                    return redirect('cart_detail')
                
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                
                product = item.product
                product.stock_quantity -= item.quantity
                product.save()
            
            order.update_total_price()
            
            cart.clear()
            
            messages.success(request, "Your order has been placed successfully!")
            return redirect('order_detail', order_id=order.id)
    else:
        initial_data = {
            'shipping_address': request.user.address,
            'phone': request.user.phone,
        }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'title': 'Checkout',
        'cart': cart,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    search_query = request.GET.get('search')
    if search_query:
        orders = orders.filter(id__icontains=search_query)
    
    context = {
        'title': 'Order History',
        'orders': orders,
        'search_query': search_query,
    }
    return render(request, 'orders/order_history.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'title': f'Order #{order.id}',
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)
