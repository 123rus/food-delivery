from email import message
from multiprocessing import context
from re import S
from unicodedata import category
from xxlimited import foo
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from core.models import FoodCard, Category, ProductsCart
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def base(request):
    categories = Category.objects.all()
    foodCards = FoodCard.objects.all()
    context = {'foodCards':foodCards, 'categories':categories}
    return render(request,'index.html', context=context)


def test(request, id):
    categories = Category.objects.all()
    category = Category.objects.get(id=id)
    print(categories)
    return render(request, 'index.html', {'categories' :categories, 'category' :category})


def product(request, id):
    foodcard = FoodCard.objects.get(id=id)
    one_type_categories = FoodCard.objects.all().filter(category=foodcard.category)
    return render(request, 'product.html', {'foodcard':foodcard, 'one_type_categories':one_type_categories})


def addCard(request, pk):
    cart_session = request.session.get('cart_session', [])
    cart_session.append(pk)
    request.session['cart_session'] = cart_session
    return redirect('base')
    # for i in products_Cart:
    #     p_name = i.name
    #     p_count = cart_products.count(i.id)
    #     p_price = i.price
    #     p_description = i.description
    #     total_sum = cart_products.count(i.id) * i.price
    #     context = {
    #         'p_name':p_name,
    #         'p_count':p_count,
    #         'p_price':p_price,
    #         'p_description':p_description,
    #         'total_sum':total_sum,
    #         'products_Cart':products_Cart
    #     }

    # print('sd',res[pk])
    # product = FoodCard.objects.get(id=pk)
    # product_cart = ProductsCart()
    # # product_cart.user = User.last_name
    # product_cart.product = product.name
    # product_cart.photo = product.image.url
    # product_cart.price = product.price
    # # for i in cart_products:
    # #     if i in res:
    # #         res[i] += 1
    # #     else:
    # #         res[i] = 1
    # print(cart_products)
    # product_cart.count = res[pk]
    # product_cart.total_sum = product_cart.price * product_cart.count
    # product_cart.save()
    # print(product)



def cart(request):
    cart_session = request.session.get('cart_session', [])
    count_of_product = len(cart_session)
    products_cart = FoodCard.objects.filter(id__in=cart_session)
    all_products_sum = 0
    for i in products_cart:
        i.count = cart_session.count(i.id)
        i.sum = i.count * i.price
        all_products_sum += i.sum   

    return render(request, 'cart.html', {'products':products_cart,
                                         'all_products_sum':all_products_sum,
                                         'count_of_product':count_of_product})


def removeCart(request,id):
    cart = request.session.get('cart_session', [])
    new_cart = []
    for pk in cart:
        if pk != id:
            new_cart.append(pk)

    request.session['cart_session'] = new_cart
    return redirect('cart')




def about(request): 
    return render(request, 'about.html')


def search(request):
    if request.method == 'POST':
        searched_product = request.POST.get('search').title()
        # product = FoodCard.objects.get(name=searched_product)
        products = FoodCard.objects.filter(name__contains = searched_product)
        
        print(products)
        # print(product.price)
        print(searched_product)
        return render(request, 'search.html',
        {'searched_product':searched_product, 'products':products})



def signup(request):
    if request.method == 'POST':
        user = UserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            return redirect('base')


    else:
        user = UserCreationForm()

    return render(request, 'auth.html', {'user':user})

def signin(request):
    return render 

def signout(request):
    return render 