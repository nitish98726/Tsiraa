from django.db import models
from accounts.models import User
from store.models import Product , Size , Color , Category
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250 , blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    size= models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=20,blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    cart = models.ForeignKey(Cart , on_delete = models.SET_NULL ,null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.product_name
    
    def item_wise_total(self):
        item_wise_total = (self.quantity*self.product.price)
        return item_wise_total
    
class Tax(models.Model):
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    tax_name = models.CharField(max_length=10)
    percent = models.FloatField(max_length=5)

    def __str__(self):
        return self.tax_name
    class Meta:
        verbose_name = "TAX"
        verbose_name_plural = "Taxes"