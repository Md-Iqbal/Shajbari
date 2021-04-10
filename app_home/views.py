from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib import messages
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Setting, ContactMessage, FAQ
from app_product.models import Product
from .forms import ContactMessageForm, SearchForm
from app_product.models import Category
# Create your views here.


def IndexView(request):
    setting = Setting.objects.get(pk=1)
    top_categories = Category.objects.all().order_by('-id')[:3]  # first 3 category
    HomeSliders = Product.objects.all().order_by('?')[:4]  # random 4
    featured_products = Product.objects.all().order_by('?')[:6]  # random 6
    latest_collections = Product.objects.all().order_by('-id')[:7]  # last 7 
    context = {
        'setting': setting,
        'top_categories': top_categories,
        'HomeSliders': HomeSliders,
        'featured_products': featured_products,
        'latest_collections': latest_collections,
    }
    return render(request, 'home/index.html', context)


def AboutusView(request):
    setting = Setting.objects.get(pk=1)
    # category = Category.objects.all()

    context = {
        'setting': setting,
        # 'category': category,
    }
    return render(request, 'home/about.html', context)


def ContactView(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            response = ContactMessage()
            response.name = form.cleaned_data['name']
            response.email = form.cleaned_data['email']
            response.subject = form.cleaned_data['subject']
            response.message = form.cleaned_data['message']
            response.ip = request.META.get('REMOTE_ADDR')
            response.save()
            messages.success(
                request, "Your message has been sent to admin. Thank you for your response.")
            return HttpResponseRedirect(reverse('Home:ContactView'))
    setting = Setting.objects.get(pk=1)
    form = ContactMessageForm
    # category = Category.objects.all()
    context = {
        'setting': setting,
        # 'category': category,
        'form': form,
    }
    return render(request, 'home/contacts.html', context)


def CategoryView(request, id, slug):
    products = Product.objects.filter(category_id=id)
    catdata = Category.objects.get(pk=id)
    you_may_like_products = Product.objects.all().order_by('?')[:6]  # random 6
    context = {
        'products': products,
        'you_may_like_products': you_may_like_products,
        'catdata': catdata,
    }
    return render(request, 'home/category_products.html', context)


def SearchView(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            products = Product.objects.filter(title__icontains=query)

            #paginator
            page = request.GET.get("page")
            paginator = Paginator(products, 5)
            try:
                products=paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
        # category = Category.objects.all()
        context = {
            'page':page,
            'query': query,
            'products': products,
            # 'category': category,
        }
        return render(request, 'home/search-results.html', context)
    return HttpResponseRedirect(reverse('Home:IndexView'))


def SearchAutoView(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Place.objects.filter(title__icontains=q)
        results = []
        for product in products:
            products_json = {}
            products_json = product.title + "," + product.state
            results.append(products_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def faqView(request):
    setting = Setting.objects.get(pk=1)
    faqs = FAQ.objects.filter(status=True).order_by("ordernumber")
    context = {
        'faqs': faqs,
        'setting': setting,
    }
    return render(request, 'home/faq.html', context)
