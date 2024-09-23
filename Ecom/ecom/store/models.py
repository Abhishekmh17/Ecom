from django.db import models
from django.contrib.auth.forms import UserCreationForm
import datetime
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural='Categories'

class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.first_name}  {self.last_name}'
    
    

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    price=models.DecimalField(default=0,decimal_places=2,max_digits=15)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,default=1) #default category is 1
    description=models.CharField(max_length=250,default='',blank=True,null=True)
    image=models.ImageField(upload_to='uploads/product/')
    
    #add sale stuff
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0,decimal_places=2,max_digits=15)
    

    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    #product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    #quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)
    date=models.DateField(default=datetime.datetime.today)
    #total_price=models.DecimalField(default=self.Cart.total_price)
    #status=models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.customer)
    
    
    
class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    

    
    
