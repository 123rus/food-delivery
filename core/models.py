from distutils.command.upload import upload
from pydoc import describe
from tabnanny import verbose
from django.db import models
from django.forms import IntegerField
from django.contrib.auth.models import User



class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Категория')
    def __str__(self):
        return self.title



# Create your models here.


class FoodCard(models.Model):
    name = models.CharField(max_length=25, verbose_name='Название еды')
    description = models.TextField(verbose_name="Описание")
    price = models.IntegerField(verbose_name='Цена')
    image = models.ImageField(upload_to='core', verbose_name='Изображение')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    


    def __str__(self):
        return self.name


class ProductsCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='cart', blank=True, null=True)
    count = models.IntegerField()
    price = IntegerField()
    total_sum = IntegerField()


    class Meta:
        verbose_name_plural = "Product's cart"
        verbose_name = "Product's cart"