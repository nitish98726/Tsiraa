from django.db import models
from store.models import Product
from accounts.models import User
# Create your models here.
class ReviewRating(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    subject = models.CharField(max_length=200 , blank=True)
    review = models.TextField(max_length=1000 , blank=True)
    rating = models.FloatField()
    image1 =models.ImageField(upload_to='customer_reviews/images' ,blank=True)
    image2 =models.ImageField(upload_to='customer_reviews/images' ,blank=True)
    image3 =models.ImageField(upload_to='customer_reviews/images' ,blank=True)
    image4 =models.ImageField(upload_to='customer_reviews/images' ,blank=True)
    ip =models.CharField(max_length=20 , blank=True)
    status =models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject