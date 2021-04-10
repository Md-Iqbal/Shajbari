from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


from app_product.models import Product
# Create your models here.

class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="cart")
    quantity = models.IntegerField()
    purchased = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        # another method of string representation
        return f'{self.product} X {self.quantity}'
    @property
    def Unit_Price(self):
        return format(self.product.price, '0.2f')
    @property
    def Sub_Total_Amount(self):
        return format(self.quantity*self.product.price, '0.2f')
    @property
    def get_totals(self):
        total = 0.0
        for sub_price in self.Sub_Total_Amount.all():
            total += sub_price
        return total

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Processing', 'Processing'),
        ('Shipping', 'Shipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    # orderitems = models.ManyToManyField(ShopCart)
    # orderitems = models.ForeignKey(ShopCart, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # ordered = models.BooleanField(blank=True, null=True, default=False)
    transactionId = models.CharField(
        max_length=255, editable=False, blank=True, null=True)
    orderTrackingId = models.CharField(max_length=255, editable=False, blank=True, null=True)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    email = models.CharField(blank=True, max_length=40)
    phone = models.CharField(blank=True, max_length=20)
    address = models.TextField(blank=True, max_length=250)
    zipcode = models.TextField(blank=True, null=True, max_length=10)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    total = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    admin_note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "order of "+self.user.username
    
    # def get_totals(self):
    #     total = 0
    #     for order_item in self.orderitems.all():
    #         total += float(order_item.Sub_Total_Amount())
    #     return total

    # def is_fully_filled(self):
    #     field_names = [f.name for f in self._meta.get_fields()]

        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True
    
class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title
    

class Wishlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="wishlist")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="wishlist")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # another method of string representation
        return f'{self.product}'

    @property
    def Unit_Price(self):
        return format(self.product.price, '0.2f')
