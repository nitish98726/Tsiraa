from django.contrib import admin
from .models import User , UserProfile , Address
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email' ,'first_name', 'last_name' , 'username' ,'last_login' , 'date_joined' , 'is_active')
    ordering = ('-date_joined',)
    list_display_links = ('email' , 'first_name' , "last_name" , 'username',)
    filter_horizontal =()
    list_filter = ()
    fieldsets = ()

admin.site.register(User , AccountAdmin)
admin.site.register(Address)
admin.site.register(UserProfile)