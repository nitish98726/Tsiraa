from django.contrib import admin
from .models import Cart , CartItem , Tax
# Register your models here.
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user' , 'product' , 'size' , 'color' , 'quantity']
    search_fields= ['user' , 'product']

class TaxAdmin(admin.ModelAdmin):
    list_display = ['category' , 'tax_name' , 'percent']
admin.site.register(Cart)
admin.site.register(CartItem , CartItemAdmin)
admin.site.register(Tax , TaxAdmin)