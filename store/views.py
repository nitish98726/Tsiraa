from django.shortcuts import render , redirect
from .models import Category , Product , Size , Color , ProductAddInfo
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize , deserialize
# Create your views here.
def category(request):
    category = Category.objects.all()
    context = {
        'category':category
    }
    return render(request , 'store/category.html' , context)

def products_bycategory(request , category_slug):
    
    # try:
        cat = get_object_or_404(Category , category_slug = category_slug)
        products = Product.objects.filter(category=cat , is_available=True )
        count = products.count()
        context = {
            'products':products,
            'category':cat,
            'count':count,
        }
        return render(request , 'store/products_bycategory.html' , context)
    # except:

    #     return redirect('category')
    
def product_detail(request , category_slug , product_slug):
   
        product = Product.objects.get(product_slug=product_slug , is_available=True)
        sizes = Size.objects.filter(product=product , is_available=True)
        colors = Color.objects.filter(product=product , is_available=True)
        serialized_product = serialize('json' , [product])
        #storing recently viewed products in session
        recently_viewed = request.session.get('recently_viewed' , [])
        
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
            
            
            return recently_viewed_products[::-1][:6]
        try:
            product_info = ProductAddInfo.objects.get(product=product)
        except:
            product_info=None
            
        context = {
            'product':product,
            'sizes':sizes,
            'product_info':product_info , 
            'recently_viewed':display_recently_viewed(request),
            'colors':colors,
        }
        return render(request , 'store/product_detail.html' , context)
   
        # return redirect('/store/category/'+category_slug)
    # return render(request , 'store/product_detail.html')