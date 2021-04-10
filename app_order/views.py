from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse, redirect, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import ShopCart, Order, OrderProduct, Wishlist
from .forms import ShopCartForm, OrderForm
from app_product.models import Product, Category
from app_user.models import UserProfile

#for payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt

#for email

from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

@login_required
def AddtoCartView(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    checkproduct = ShopCart.objects.filter(product_id=id)

    if checkproduct:
        control = 1
    else:
        control = 0

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
                messages.success(request, "successfuly updated the cart!")
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
                messages.success(request, "successfuly added to cart!")
        return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()  #
            messages.success(request, "successfuly updated the cart!")
        else:  # Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
            messages.success(request, "successfuly added to cart!")
        return HttpResponseRedirect(url)


@login_required
def CartListView(request):
    you_may_like_products = Product.objects.all().order_by('?')[:6]  # random 6
    current_user = request.user
    shopcarts = ShopCart.objects.filter(user_id=current_user.id)
    total_price = 0
    for shopcart in shopcarts:
        total_price += shopcart.product.price*shopcart.quantity
    context = {
        'shopcarts': shopcarts,
        'you_may_like_products': you_may_like_products,
        'total_price': total_price,
    }
    return render(request, 'order/cart.html', context)


@login_required
def DeleteCartView(request, id):
    item = ShopCart.objects.filter(product_id=id)
    item.delete()
    return HttpResponseRedirect(reverse("Order:CartListView"))


@login_required
def DeleteFullCartView(request):
    item = ShopCart.objects.all()
    item.delete()
    return HttpResponseRedirect(reverse("Order:CartListView"))


def AddtoWishlistView(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    checkproduct = Wishlist.objects.filter(product_id=id)

    if checkproduct:
        control = 1
    else:
        control = 0


    if control == 0:
        data = Wishlist()
        data.user_id = current_user.id
        data.product_id = id
        data.save()
        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(url)


def WishlistListView(request):
    you_may_like_products = Product.objects.all().order_by('?')[:6]  # random 6
    current_user = request.user
    wishlists = Wishlist.objects.filter(user_id=current_user.id)
    context = {
        'wishlists': wishlists,
        'you_may_like_products': you_may_like_products,
    }
    return render(request, 'order/wishlist.html', context)


def DeleteWishlistView(request, id):
    item = Wishlist.objects.filter(product_id=id)
    item.delete()
    return HttpResponseRedirect(reverse("Order:WishlistListView"))


def DeleteFullWishlistView(request):
    item = Wishlist.objects.all()
    item.delete()
    return HttpResponseRedirect(reverse("Order:WishlistListView"))



@login_required
def CheckoutView(request):
    url = request.META.get('HTTP_REFERER')
    # category = Category.objects.all()
    current_user = request.user
    shopcarts = ShopCart.objects.filter(user_id=current_user.id)
    if shopcarts.exists():
        total_price = 0
        for order in shopcarts:
            total_price += order.product.price*order.quantity
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                data = Order()
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.city = form.cleaned_data['city']
                data.country = form.cleaned_data['country']
                data.zipcode = form.cleaned_data['zipcode']
                data.email = form.cleaned_data['email']
                data.phone = form.cleaned_data['phone']
                data.address = form.cleaned_data['address']
                data.user_id = current_user.id
                data.total = total_price
                data.ip = request.META.get('REMOTE_ADDR')
                orderId = get_random_string(13).upper()
                data.save()
                shopcarts = ShopCart.objects.filter(user_id=current_user.id)
                for cart in shopcarts:
                    detail = OrderProduct()
                    detail.order_id = data.id  # Order Id
                    detail.product_id = cart.product_id
                    detail.user_id = current_user.id
                    detail.quantity = cart.quantity
                    detail.price = cart.product.price
                    detail.amount = cart.Sub_Total_Amount
                    detail.save()
                    product = Product.objects.get(id=cart.product_id)
                    product.amount -= cart.quantity
                    product.save()
                context={
                    'orderId':orderId,
                }
                return HttpResponseRedirect(reverse('Order:PaymentView'))
            else:
                messages.warning(request, form.errors)
                return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(reverse('Home:IndexView'))
    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    # saved_adress = Order.objects.filter(user=current_user)
    # saved_adress=saved_adress[0]
    context = {
        'shopcarts':shopcarts,
        'total_price':total_price,
        # 'category': category,
        'profile': profile,
        'form':form,
        # 'saved_adress': saved_adress,
    }
    return render(request, 'order/checkout_review&address.html', context)


@login_required
def PaymentView(request):
    cart = ShopCart.objects.filter(user_id=request.user.id)
    if cart.exists():
        # Clear & Delete shopcart
        cart.delete()
        request.session['cart_items'] = 0
        last_order = Order.objects.last()
        order_query = OrderProduct.objects.filter(order_id=last_order.pk)
        store_id = 'shajb606c38852a3a2'
        api_key = 'shajb606c38852a3a2@ssl'
        mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
                                sslc_store_pass=api_key)
        #status_url = request.build_absolute_uri()  #for getting running view url
        status_url = request.build_absolute_uri(
            reverse('Order:Order_PaymentComplete'))
        print(status_url)
        mypayment.set_urls(success_url=status_url, fail_url=status_url,
                        cancel_url=status_url, ipn_url=status_url)
        # for query in order_query:
        #     order_items.add(query)
        # order_items = order_query[0]
        order_items_count = order_query.count()
        # price_query = ShopCart.objects.filter(user_id=request.user.id)
        # print(price_query)
        total_price = 0
        for price in order_query:
            total_price += price.amount
        mypayment.set_product_integration(total_amount=Decimal(total_price), currency='BDT', product_category='Mixed',
                                        product_name=order_query, num_of_item=order_items_count, shipping_method='Local Shipping', product_profile='None')
        customer_info = Order.objects.last()
        if customer_info.first_name is None:
            return redirect("Order:CheckoutView")
        elif customer_info.last_name is None:
            return redirect("Order:CheckoutView")
        elif customer_info.email is None:
            return redirect("Order:CheckoutView")
        elif customer_info.city is None:
            return redirect("Order:CheckoutView")
        elif customer_info.zipcode is None:
            return redirect("Order:CheckoutView")
        elif customer_info.country is None:
            return redirect("Order:CheckoutView")
        elif customer_info.phone is None:
            return redirect("Order:CheckoutView")
        elif customer_info.address is None:
            return redirect("Order:CheckoutView")
        mypayment.set_customer_info(name=customer_info.first_name+ customer_info.last_name, email=customer_info.email, address1=customer_info.address,
                                    address2=customer_info.address, city=customer_info.city, postcode=customer_info.zipcode, country=customer_info.country, phone=customer_info.phone)
        mypayment.set_shipping_info(shipping_to=customer_info.first_name+customer_info.last_name, address=customer_info.address,
                                    city=customer_info.city, postcode=customer_info.zipcode, country=customer_info.country)

        response_data = mypayment.init_payment()
    else:
        return HttpResponseRedirect(reverse('Home:IndexView'))
    context={

    }
    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def Order_PaymentComplete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']
        print(status)
        # amount = payment_data['amount']
        # amount = payment_data['amount']
        # amount = payment_data['amount']
        # amount = payment_data['amount']
        # amount = payment_data['amount']
        # amount = payment_data['amount']
        # amount = payment_data['amount']
        # amount = payment_data['amount']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']

            customer_info = Order.objects.last()
            paid_amount = customer_info.total
            name = customer_info.first_name+" "+customer_info.last_name
            subject = 'Thanks for purchasing the ShajBari goods'
            message = f'Hi {name}, payement of BDT {paid_amount} is successfull. your transaction id is: {tran_id} and order tracking no is: {val_id}. Have a good day!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [customer_info.email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(
                request, f"Your Payement Was Successful! Check your mail to see payment details. You'll be redirected to home page within 10 seconds.")
        if status == 'Not Safe':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']

            customer_info = Order.objects.last()
            name = customer_info.first_name+" "+customer_info.last_name
            subject = 'Thanks for purchasing the ShajBari goods'
            message = f'Hi {name}, your transaction id is : {tran_id} and order tracking no is : {val_id}. Have a good day!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [customer_info.email, ]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(
                request, f"Your order is successful but payment in pending! Check your mail to see payment details. Please Try Again! You'll be redirected to home page within 10 seconds.")
        if status == 'FAILED':
            Order.objects.last().delete()
            messages.success(
                request, f"Your Payement Was Unsuccessful! Please Try Again! You'll be redirected to home page within 10 seconds.")
    if val_id and tran_id:
        order = Order.objects.last()
        order.orderId=val_id
        order.transactionId=tran_id
        order.save()
        context={
            'status': status,
            'val_id': val_id,
            'tran_id': tran_id,
        }
    return render(request, 'order/order_complete.html', context)
