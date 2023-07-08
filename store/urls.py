from django.urls import path
from . import views

urlpatterns = [
    path('category/' , views.category ,name='category'),
    path('category/<slug:category_slug>/' , views.products_bycategory , name='products_bycategory'),
    path('product_detail/<slug:category_slug>/<slug:product_slug>/' , views.product_detail , name ='product_detail')
]