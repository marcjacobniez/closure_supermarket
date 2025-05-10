from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import Category, Product
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample data for Closure\'s Online Supermarket'

    def handle(self, *args, **kwargs):
        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        
        # Create categories
        categories = [
            {'name': 'Fruits & Vegetables', 'description': 'Fresh fruits and vegetables'},
            {'name': 'Dairy & Eggs', 'description': 'Milk, cheese, butter, and eggs'},
            {'name': 'Bakery', 'description': 'Bread, cakes, and pastries'},
            {'name': 'Meat & Seafood', 'description': 'Fresh meat and seafood'},
            {'name': 'Beverages', 'description': 'Drinks and juices'},
            {'name': 'Snacks', 'description': 'Chips, cookies, and more'},
        ]
        
        created_categories = []
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            created_categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category "{category.name}" created'))
        
        # Create products for each category
        products_data = {
            'Fruits & Vegetables': [
                {'name': 'Apples', 'price': Decimal('2.99'), 'stock': 100},
                {'name': 'Bananas', 'price': Decimal('1.49'), 'stock': 150},
                {'name': 'Carrots', 'price': Decimal('1.99'), 'stock': 80},
                {'name': 'Potatoes', 'price': Decimal('3.49'), 'stock': 120},
                {'name': 'Lettuce', 'price': Decimal('1.79'), 'stock': 50},
            ],
            'Dairy & Eggs': [
                {'name': 'Milk', 'price': Decimal('2.49'), 'stock': 100},
                {'name': 'Eggs', 'price': Decimal('3.99'), 'stock': 80},
                {'name': 'Cheese', 'price': Decimal('4.99'), 'stock': 60},
                {'name': 'Yogurt', 'price': Decimal('1.29'), 'stock': 90},
                {'name': 'Butter', 'price': Decimal('3.49'), 'stock': 70},
            ],
            'Bakery': [
                {'name': 'Bread', 'price': Decimal('2.29'), 'stock': 100},
                {'name': 'Bagels', 'price': Decimal('3.99'), 'stock': 50},
                {'name': 'Muffins', 'price': Decimal('4.49'), 'stock': 40},
                {'name': 'Croissants', 'price': Decimal('5.99'), 'stock': 30},
                {'name': 'Cake', 'price': Decimal('12.99'), 'stock': 20},
            ],
            'Meat & Seafood': [
                {'name': 'Chicken Breast', 'price': Decimal('6.99'), 'stock': 60},
                {'name': 'Ground Beef', 'price': Decimal('5.99'), 'stock': 50},
                {'name': 'Salmon', 'price': Decimal('9.99'), 'stock': 40},
                {'name': 'Shrimp', 'price': Decimal('11.99'), 'stock': 30},
                {'name': 'Pork Chops', 'price': Decimal('7.49'), 'stock': 45},
            ],
            'Beverages': [
                {'name': 'Water (12-pack)', 'price': Decimal('4.99'), 'stock': 100},
                {'name': 'Soda (6-pack)', 'price': Decimal('3.99'), 'stock': 80},
                {'name': 'Orange Juice', 'price': Decimal('2.99'), 'stock': 60},
                {'name': 'Coffee', 'price': Decimal('7.99'), 'stock': 50},
                {'name': 'Tea', 'price': Decimal('3.49'), 'stock': 70},
            ],
            'Snacks': [
                {'name': 'Potato Chips', 'price': Decimal('2.99'), 'stock': 100},
                {'name': 'Chocolate Cookies', 'price': Decimal('3.49'), 'stock': 80},
                {'name': 'Popcorn', 'price': Decimal('1.99'), 'stock': 90},
                {'name': 'Pretzels', 'price': Decimal('2.49'), 'stock': 70},
                {'name': 'Trail Mix', 'price': Decimal('4.99'), 'stock': 60},
            ],
        }
        
        products_created = 0
        for category in created_categories:
            if category.name in products_data:
                for product_data in products_data[category.name]:
                    product, created = Product.objects.get_or_create(
                        name=product_data['name'],
                        category=category,
                        defaults={
                            'description': f'This is a {product_data["name"]} product in the {category.name} category.',
                            'price': product_data['price'],
                            'stock_quantity': product_data['stock'],
                            'available': True,
                        }
                    )
                    if created:
                        products_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {products_created} new products'))