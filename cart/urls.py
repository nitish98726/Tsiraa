from django.urls import path
from . import views
urlpatterns = [
    path('' , views.cart , name='cart'),
    # Add to cart from product detail page
    path('add_cart/<int:product_id>/' , views.add_cart , name='add_cart'),
    # Add to cart from cart Page
    path('add_cart_ajax/<int:cart_item_id>/' , views.add_cart_ajax , name='add_cart_ajax'),
    # Decrease cart Items in cart Page
    path('decrease_cart/<int:cart_item_id>/' , views.decrease_cart , name='decrease_cart'),
    # Remove cart Item
    path('remove_cart/<int:cart_item_id>/' , views.remove_cart , name='remove_cart'),
    path('checkout/', views.checkout , name='checkout'),
]