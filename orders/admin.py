from django.contrib import admin
from .models import Order , OrderProduct , Payment
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user' , 'full_name' , 'order_number' , 'tax' , 'order_total']
admin.site.register(Order , OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)