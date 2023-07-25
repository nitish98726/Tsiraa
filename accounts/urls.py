from django.urls import path
from . import views

urlpatterns = [
    path("", views.accounts, name="accounts"),
    path('login/' , views.login , name='login'),
    path('register/' , views.register , name='register'),
    path('logout/' , views.logout , name='logout'),
    path('forgotPassword/' , views.forgotPassword , name= 'forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>' , views.reset_password_validate , name= 'reset_password_validate'),
    path('reset_password/' , views.reset_password , name = 'reset_password'),
    path('custDashBoard/' , views.custDashboard , name='custDashboard'),
    path('custProfile/' , views.custProfile , name='custProfile'),
    path('address/' , views.address , name='address'),
    # path('save_address/' , views.save_address , name='save_address')
]
