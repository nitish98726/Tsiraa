from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import ProductAddInfo
from django.db.models import Q
def home(request):
    return render(request, "home.html")

def search(request):
    if request.method == 'GET':
        search = request.GET['search']
        products_byinfo = ProductAddInfo.objects.filter(Q(product__product_name__icontains = search ,product__is_available=True) | Q(product__description__icontains=search) | Q(description__icontains=search))
        count = products_byinfo.count()
        # print(products)
        context = {
            'products_byinfo':products_byinfo,
            # 'category':cat,
            'count':count,
        }
    return render(request , 'store/product_search.html' , context)

def customer_care(request):
    return render(request , 'customer_care.html')

def faq(request):
    return render(request , 'faq.html')

def privacy_policy(request):
    return render(request , 'privacy_policy.html')