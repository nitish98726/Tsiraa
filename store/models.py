from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50 , unique=True)
    category_slug = models.SlugField(max_length=50 , unique=True)
    category_createdBy = models.CharField(max_length=50 , blank=True)
    category_description = models.CharField(max_length=500 , blank=True)
    category_image = models.ImageField(upload_to='photos/categories')
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
   
    
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.category_name
    def get_url(self):
        return reverse('products_bycategory' ,args=[self.category_slug])



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50 , unique=True)
    product_slug = models.SlugField(max_length=200 , unique=True)
    description = models.TextField(max_length=150 , blank=True)
    
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    product_createdBy = models.CharField(max_length=50 , blank=True)
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    # function to check when stock less than or equal to zero
    def save(self , *args , **kwargs):
        if self.stock <=0 :
            self.is_available=False
        else:
            self.is_available=True
            
        super().save(*args , **kwargs)
    
    def __str__(self):
        return self.product_name
        

class Size(models.Model):
    product  = models.ForeignKey(Product , on_delete=models.CASCADE)
    stock = models.IntegerField()
    size = models.CharField(max_length=10 , blank=True)
    size_slug = models.SlugField(max_length=20 ,blank=True)
    size_createdBy = models.CharField(max_length=50 , blank=True)
    is_available = models.BooleanField(default=True)
    description = models.CharField(max_length=200 ,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.size

    def save(self , *args , **kwargs):
        if self.stock <=0 :
            self.is_available=False
        else:
            self.is_available=True
        super().save(*args , **kwargs)

    

class Color(models.Model):
    product  = models.ForeignKey(Product , on_delete=models.CASCADE)
    size = models.ForeignKey(Size , on_delete=models.CASCADE)
    stock = models.IntegerField()
    color_createdBy = models.CharField(max_length=50 , blank=True)
    color = models.CharField(max_length=10 )
    color_slug = models.SlugField(max_length=30 , blank=True)
    color_desName = models.CharField(max_length =20 , blank=True)
    is_available = models.BooleanField(default=True)
    description = models.CharField(max_length = 200 ,  blank=True)
    
   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.color
    
    def save(self , *args , **kwargs):
        if self.stock <=0 :
            self.is_available=False
        else:
            self.is_available=True
            
        super().save(*args , **kwargs)

class ProductGallery(models.Model):
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products')
    size = models.ForeignKey(Size, null=True,on_delete=models.SET_NULL)
    color = models.ForeignKey(Color ,null=True , on_delete=models.SET_NULL)
    gallery_createdBy = models.CharField(max_length =50 ,blank=True)
    class Meta:
        verbose_name = "Image Gallery"
        verbose_name_plural = 'Image Gallery'
    
    def __str__(self):
        return self.product.product_name

class ProductAddInfo(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    description = models.TextField(max_length=1000 , blank=True)
    available_packaging = models.CharField(max_length=200 , blank=True)
    weight = models.CharField(max_length=50)
    dimensions = models.CharField(max_length=50)
    brand = models.CharField(max_length=20 , blank=True)
    class Meta:
        verbose_name = "Product Additional Info"
        verbose_name_plural = "Product Additional Info"

    def __str__(self):
        return self.product.product_name