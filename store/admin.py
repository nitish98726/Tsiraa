from django.contrib import admin
from .models import Category , Product , Size , Color , ProductGallery , ProductAddInfo

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'product_slug':('product_name' ,)}
    list_display = ['category' , 'product_name' ,'price' ,'stock' , 'is_available' , 'created_at']
    
    list_filter = ['category' , 'is_available']
    list_editable=['is_available']




admin.site.register(Category)
admin.site.register(Product , ProductAdmin)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ProductGallery)
admin.site.register(ProductAddInfo)