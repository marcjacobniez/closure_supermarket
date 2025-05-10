from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Cart

# basically, for every user, there's always a cart for them

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)