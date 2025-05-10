from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    User registration
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'address')

class CustomUserChangeForm(UserChangeForm):
    """
    User information update
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'address')

class ProfileUpdateForm(forms.ModelForm):
    """
    Incase they want to change profile
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'address']