from queue import PriorityQueue
from django.contrib import admin
from .models import Category, FoodCard, ProductsCart
# Register your models here.
admin.site.register(Category)
admin.site.register(FoodCard)
admin.site.register(ProductsCart)