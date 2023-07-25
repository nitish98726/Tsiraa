from django.db import models
from accounts.models import User
from store.models import Product
# Create your models here.
# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    payment_id= models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id
        
class Order(models.Model):
    STATUS =(
        ("New" , "New"),
        ("Accepted","Accepted"),
        ("Completed","Completed"),
        ("Cancelled" , "Cancelled"),
    )

    user = models.ForeignKey(User , on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment , on_delete=models.CASCADE ,blank=True , null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length = 50)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=70 , blank=True)
    landmark=  models.CharField(max_length=50 , blank=True)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    zip = models.CharField(max_length=10 , null=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10 ,choices=STATUS , default="NEW")
    ip = models.CharField(blank= True , max_length = 20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    def full_address(self):
        return f'{self.address_line1} {self.address_line2} {self.state} {self.city} {self.zip}'
    
    
    
    def __str__(self):
        return self.first_name

class OrderProduct(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment , on_delete=models.SET_NULL , blank=True , null=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    size = models.CharField(max_length=10 , blank=True , null=True)
    color = models.CharField(max_length=20 , blank=True , null=True)
    quantity = models.IntegerField()
    productPrice = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def product_total(self):
        return (self.product.price*self.quantity)

    def __str__(self):
        return self.product.product_name

