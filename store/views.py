from django.shortcuts import render , redirect
from .models import Category , Product , Size , Color , ProductAddInfo
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize , deserialize
from django.http import JsonResponse
import requests
from django.conf import settings
from reviews.models import ReviewRating
from django.core.paginator import Paginator

# Create your views here.
def category(request):
    category = Category.objects.all()
    context = {
        'category':category
    }
    return render(request , 'store/category.html' , context)

def products_bycategory(request , category_slug):
    
    try:
        cat = get_object_or_404(Category , category_slug = category_slug)
        products = Product.objects.filter(category=cat , is_available=True )
        count = products.count()
        paginator = Paginator(products , 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {
            'products':paged_products,
            'category':cat,
            'count':count,
        }
        return render(request , 'store/products_bycategory.html' , context)
    except:

        return redirect('category')
    
def product_detail(request , category_slug , product_slug):
   
        product = Product.objects.get(product_slug=product_slug , is_available=True)
        sizes = Size.objects.filter(product=product , is_available=True)
        colors = Color.objects.filter(product=product , is_available=True)
        serialized_product = serialize('json' , [product])
        #storing recently viewed products in session
        recently_viewed = request.session.get('recently_viewed' , [])
        # fetching last 6
        if serialized_product in recently_viewed[-6:]:
            pass
        else:
            recently_viewed.append(serialized_product)
        
        request.session['recently_viewed'] = recently_viewed
        def display_recently_viewed(request):
            # Get the recently viewed products from the session
            recently_viewed_data = request.session.get('recently_viewed', [])
            # Deserialize each serialized product back into a Product object
            recently_viewed_products = []
            for serialized_product in recently_viewed_data:
                deserialized_products = list(deserialize('json', serialized_product))
                for deserialized_product in deserialized_products:
                    recently_viewed_products.append(deserialized_product.object)
            
            
            return recently_viewed_products[::-1][:6] #reversing and showing last6
        try:
            product_info = ProductAddInfo.objects.get(product=product)
        except:
            product_info=None
        
        # Get the product Reviews for Product Detail Page
        reviews = ReviewRating.objects.filter(product = product ,status=True)
        
        context = {
            'product':product,
            'sizes':sizes,
            'product_info':product_info , 
            'recently_viewed':display_recently_viewed(request),
            'colors':colors,
            'reviews':reviews,
        }
        return render(request , 'store/product_detail.html' , context)
   
        # return redirect('/store/category/'+category_slug)
    # return render(request , 'store/product_detail.html')

def products(request):
    products_list= []
    category = Category.objects.all()
    # merged_queryset = Product.objects.none()
    for cat in category:
        products = Product.objects.filter(category__category_slug=cat.category_slug , is_available=True).order_by('-created_at')[:5]
        products_list.append(products)
    merged_queryset = products_list[0]
    
    for products in products_list[1:]:
        merged_queryset = merged_queryset.union(products)
    
    paginator = Paginator(merged_queryset , 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    # print(products_list)
    context = {
        'products' :paged_products,
    }
    return render(request , 'store/products.html' , context)

# Check pin code servicable or not
def service_pincode(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        pin_code = request.GET['pin_code']
        # print(pin_code)
        url = 'https://track.delhivery.com/c/api/pin-codes/json/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token '+settings.DEL_TOKEN
        }
        params = {
            'filter_codes': pin_code
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
       
            return JsonResponse({
                'status':'Success',
                'data':data,
            })
        except:
            return JsonResponse({
                'status':"Failed",
                "message":"Pin Code Incorrect or not servicabe "
            })