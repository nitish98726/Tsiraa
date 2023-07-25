from django.urls import path
from . import views
urlpatterns = [
    path('' , views.order ,name = 'order'),
    path('payment/' , views.payment , name ='payment'),
    path('order_complete/' , views.order_complete , name='order_complete'),
]