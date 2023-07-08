from django.urls import path
from . import views
urlpatterns = [
    path('' , views.cart , name='cart'),
    path('add_cart/<int:product_id>/' , views.add_cart , name='add_cart'),
    path('add_cart_ajax/<int:cart_item_id>/' , views.add_cart_ajax , name='add_cart_ajax'),
    path('checkout/', views.checkout , name='checkout'),
]