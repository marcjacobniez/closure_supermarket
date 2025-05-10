from django.db import models
from django.conf import settings
from store.models import Product

class Order(models.Model):
    """
    Customer orders or somkething
    """
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_address = models.TextField()
    phone = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
    def get_total_cost(self):
        """Sum of the order"""
        return sum(item.get_cost() for item in self.items.all())
    
    def update_total_price(self):
        """I forgot what this does but something something total price based on order items"""
        self.total_price = self.get_total_cost()
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_cost(self):
        """Calculate cost of this order item"""
        return self.price * self.quantity

class Cart(models.Model):
    """
    The cart (Very important)
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart - {self.user.username}"
    
    def add_item(self, product, quantity=1):
        """Add item to cart case of the user adding more to the quantity"""
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        return cart_item
    
    def remove_item(self, product):
        """Remove item from cart"""
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
            cart_item.delete()
            return True
        except CartItem.DoesNotExist:
            return False
            
    def update_item_quantity(self, product, quantity):
        """Obv change the quantity"""
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
            cart_item.quantity = quantity
            cart_item.save()
            return cart_item
        except CartItem.DoesNotExist:
            return None
    
    def clear(self):
        """Clear all"""
        self.items.all().delete()
    
    def get_total_price(self):
        """Same as before"""
        return sum(item.get_price() for item in self.items.all())
    
    def get_item_count(self):
        """And same as before"""
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    """
    Individual items in a cart
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_price(self):
        """Calculate price of items obv"""
        return self.product.price * self.quantity