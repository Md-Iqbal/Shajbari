from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import GalleryImage, Product, Category, Comment
from app_home.models import Setting
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
# Create your views here.


def ShopView(request):
    setting = Setting.objects.get(pk=1)
    products = Product.objects.all()
    #paginator
    page = request.GET.get("page")
    paginator = Paginator(products, 12)
    try:
        products=paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'products':products,
        'setting':setting,
    }
    return render(request, 'product/shop.html', context)


def ProductDetailView(request, slug):
    you_may_like_products = Product.objects.all().order_by('?')[:6]  # random 6
    product = Product.objects.get(slug=slug)
    # category = Category.objects.all()
    images = GalleryImage.objects.filter(product_id=product.id)
    comments = Comment.objects.filter(product_id=product.id)
    context = {
        'product': product,
        'you_may_like_products': you_may_like_products,
        # 'category': category,
        'images': images,
        'comments': comments,
    }
    return render(request, 'product/product-detail.html', context)


@login_required
def MakeCommentView(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.product_id=id
            current_user= request.user
            data.user_id=current_user.id
            data.save()  # save data to table
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)
