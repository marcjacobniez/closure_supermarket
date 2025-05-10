from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    CUSTOMER = 'customer'
    STAFF = 'staff'
    ADMIN = 'admin'
    DELIVERY = 'delivery'
    
    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (STAFF, 'Staff'),
        (ADMIN, 'Admin'),
        (DELIVERY, 'Delivery Personnel'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return self.username
    
    @property
    def is_customer(self):
        return self.role == self.CUSTOMER
    
    @property
    def is_staff_member(self):
        return self.role == self.STAFF
    
    @property
    def is_delivery_personnel(self):
        return self.role == self.DELIVERY
