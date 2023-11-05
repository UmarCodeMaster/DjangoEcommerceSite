from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class Company(models.Model):
    Company_name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.Company_name


class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    STOCK_CHOICES = (
        ('in stock', 'IN STOCK'),
        ('out of Stock', 'OUT OF STOCK'),
    )
    name = models.CharField(max_length=200)
    image = models.ImageField()
    discount_offer = models.CharField(max_length=200)
    storage = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    discription = models.TextField()
    discount_price = models.IntegerField()
    price = models.IntegerField()
    stock = models.CharField(max_length=100,choices=STOCK_CHOICES,)
    trending = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Image(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='uploads', null=True)

    def __str__(self):
        return self.product.name


User = get_user_model()

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.user}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    
    def __str__(self):
        return str(self.product)


class CheckoutCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ManyToManyField(CartItem, related_name='checkout_cart' ,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.createdAt)



class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    comp_name = models.CharField(max_length=255, null=True, blank=True)
    area_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    busines_address = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.first_name
    

