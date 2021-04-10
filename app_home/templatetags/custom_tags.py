from django import template
from app_order.models import ShopCart
from app_product.models import Category, Product
from django.db.models import Sum, Count


register = template.Library()


@register.simple_tag
def CategoryList():
    return Category.objects.all()

@register.simple_tag
def CartProductCount(userid):
    product_count = ShopCart.objects.filter(user_id=userid).count()
    return product_count


@register.simple_tag
def ProductList():
    return Product.objects.all()
