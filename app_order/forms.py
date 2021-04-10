from django import forms
from .models import ShopCart, Order

class ShopCartForm(forms.ModelForm):
    class Meta:
        model = ShopCart
        fields=['quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email' ,'address','zipcode', 'phone', 'city', 'country', 'total']