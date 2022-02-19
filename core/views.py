from multiprocessing import context
from re import S
from unicodedata import category
from xxlimited import foo
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from core.models import FoodCard, Category, ProductsCart
from django.contrib.auth.models import User


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

cart_products = []
res = {}
def addCard(request, pk):
    cart_session = request.session.get('cart_session', [])
    print(cart_session)
    
    cart_products.append(pk)
    products_Cart = FoodCard.objects.filter(id__in=cart_products)
    return HttpResponseRedirect('/')
    print(cart_products)
    print(products_Cart)
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
    products_Cart = FoodCard.objects.filter(id__in=cart_products)
    all_products_sum = 0
    for i in products_Cart:
        i.count = cart_products.count(i.id)
        i.sum = cart_products.count(i.id) * i.price
        all_products_sum += i.sum   
        count_of_product += i.count
    context = {
        'products_Cart':products_Cart,
        'all_products_sum':all_products_sum,
        'count_of_product':count_of_product
    }
    return render(request, 'cart.html', context=context)


def removeCart(request,id):
    cart_session = request.session.get('cart_session', [])
    print(cart_session)
    carts = []
    for i in cart_session:
        if id != i:
            carts.append(i)
    request.session['cart_session'] = carts
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



