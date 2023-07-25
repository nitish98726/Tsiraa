from django.urls import path
from . import views

urlpatterns = [
    path('category/' , views.category ,name='category'),
    # See Proucts By Category
    path('category/<slug:category_slug>/' , views.products_bycategory , name='products_bycategory'),
    #Product Detail Page
    path('product_detail/<slug:category_slug>/<slug:product_slug>/' , views.product_detail , name ='product_detail'),
    # All Products Page
    path('products/' , views.products ,name='products'),
    # Check pin code servicable or not
    path('service_pincode/' , views.service_pincode , name='service_pincode'),
]