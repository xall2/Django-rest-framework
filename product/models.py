from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):

    categoryList = [
        ('computers','computers'),
        ('food','food'),
        ('kids','kids'),
        ('home','home'),
    ]

    name = models.CharField(max_length=200, default="",blank=False)
    description = models.TextField(max_length=1000, default="",blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    brand = models.CharField(max_length=200, default="",blank=False)
    category = models.CharField(max_length=40, blank=False, choices=categoryList)
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User ,null=True, on_delete=models.SET_NULL)#عشان اعرف مين اليوزر اللي اضاف هذا المنتج

    def __str__(self): #سيلف يعني يقصد الكلاس اللي هوا فيه داخله
        return self.name


class Review(models.Model):
    #عشان اعرف ايش البرودكت اللي سوا تقييم
    product = models.ForeignKey(Product ,null=True, related_name='reviews', on_delete=models.CASCADE)#لان اذا المنتج انحذف راح ينحذف التقييم
    user = models.ForeignKey(User ,null=True, on_delete=models.SET_NULL)#عشان اعرف مين اليوزر اللي اضاف هذا التقييم 
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=1000, default="",blank=False)
    createAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): #سيلف يعني يقصد الكلاس اللي هوا فيه داخله
        return self.comment