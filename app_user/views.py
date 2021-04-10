from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from app_product.models import Category
from .models import UserProfile
from app_home.models import Setting
from app_order.models import Order, OrderProduct, Wishlist
from app_product.models import Comment
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .tokens import account_activation_token
# Create your views here.


def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id = current_user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect(reverse('Home:IndexView'))
        else:
            messages.warning(request, "Login error! Username or Password is wrong.")
            return HttpResponseRedirect(reverse('App_User:LoginView'))
    setting = Setting.objects.get(pk=1)
    context={
        'setting':setting,
    }
    return render(request, 'user/login.html')

@login_required
def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('Home:IndexView'))

def SignUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "users_img/default/default.jpg"
            data.save()
            # user=User.objects.create_user(username=username, email=email)
                    
            return HttpResponseRedirect(reverse('Home:IndexView'))
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(reverse('App_User:SignUpView'))
    # category = Category.objects.all()
    form = SignUpForm()
    setting = Setting.objects.get(pk=1)
    context = {
        'form':form,
        'setting': setting,
    }
    return render(request, 'user/signup.html', context)

@login_required
def ProfileView(request, username):
    comments = Comment.objects.filter(user_id=request.user.id)
    orders = Order.objects.filter(user_id=request.user.id)
    profile = UserProfile.objects.get(user_id=request.user.id)
    setting = Setting.objects.get(pk=1)
    context = {
        'comments': comments,
        'orders': orders,
        'setting': setting,
        'profile':profile,
        # 'category': category,
    }
    return render(request, 'user/profile.html', context)


@login_required
def UserInfoUpdateView(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account details has been updated!')
            return HttpResponseRedirect(url)
    else:
        # category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        setting = Setting.objects.get(pk=1)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'setting': setting,
        }
    return render(request, 'user/updateProfile.html', context)

@login_required
def UserPasswordUpdateView(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return HttpResponseRedirect(reverse('Home:IndexView'))
        else:
            messages.error(
                request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect(url)
    else:
        # category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        setting = Setting.objects.get(pk=1)
        context={
            # 'category':category,
            'form':form,
            'setting': setting,
        }
        return render(request, 'user/updatePassword.html', context)

@login_required
def OrderHistoryView(request):
    orders = Order.objects.filter(user_id=request.user.id)
    comments = Comment.objects.filter(user_id=request.user.id)
    profile = UserProfile.objects.get(user_id=request.user.id)
    setting = Setting.objects.get(pk=1)
    context = {
        'orders': orders,
        'profile': profile,
        'comments': comments,
        'setting': setting,
    }
    return render(request, 'user/my-orders.html', context)


@login_required
def WishlistHistoryView(request):
    wishlists = Wishlist.objects.filter(user_id=request.user.id)
    comments = Comment.objects.filter(user_id=request.user.id)
    profile = UserProfile.objects.get(user_id=request.user.id)
    setting = Setting.objects.get(pk=1)
    context = {
        'wishlists': wishlists,
        'profile': profile,
        'comments': comments,
        'setting': setting,
    }
    return render(request, 'user/my-wishlist.html', context)

@login_required
def UserOrderDetailView(request, id):
    comments = Comment.objects.filter(user_id=request.user.id)
    orders = Order.objects.filter(user_id=request.user.id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    # category = Category.objects.all()
    profile = UserProfile.objects.get(user_id=request.user.id)
    setting = Setting.objects.get(pk=1)
    context = {
        'profile': profile,
        # 'category': category,
        'comments': comments,
        'orders': orders,
        'orderitems': orderitems,
        'setting': setting,
    }
    return render(request, 'user/my-orders-details.html', context)


@login_required
def UserCommentListView(request):
    comments = Comment.objects.filter(user_id=request.user.id)
    orders = Order.objects.filter(user_id=request.user.id)
    # category = Category.objects.all()
    profile = UserProfile.objects.get(user_id=request.user.id)
    setting = Setting.objects.get(pk=1)
    context = {
        'profile': profile,
        # 'category': category,
        'comments': comments,
        'orders': orders,
        'setting': setting,
    }
    return render(request, 'user/my-comments.html', context)


@login_required
def DeleteCommentView(request, id):
    Comment.objects.filter(id=id, user_id=request.user.id).delete()
    return HttpResponseRedirect(reverse('App_User:UserCommentListView'))
