from email import message
from multiprocessing import AuthenticationError, context
from re import S
from unicodedata import category
from xxlimited import foo
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from core.models import Customer, FoodCard, Category, ProductsCart, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('base')
    else:
        form = AuthenticationForm()

    return render(request, 'auth.html', {'user':form})

def signout(request):
    logout(request)
    return redirect('base')


def order(request):
    if request.method == 'POST':
        cart_session = request.session.get('cart_session', [])
        if len(cart_session) == 0:
            messages.error(request, 'Ваша корзина пустая', extra_tags='danger')
            return redirect('cart')
        else: 
            customer = Customer()
            customer.name = request.POST.get('c_name')
            customer.l_name = request.POST.get('c_lname')
            customer.number = request.POST.get('c_number')
            customer.address = request.POST.get('c_address')
            customer.message = request.POST.get('c_message')
            customer.save()


            for i in range(len(cart_session)):
                order = Order()
                order.product = FoodCard.objects.get(id=cart_session[i])
                order.customer = customer
                order.price = order.product.price 
                order.phone = customer.number
                order.address = customer.address 
                order.save()

            request.session['cart_session'] = []
            messages.error(request, 'Заказ успешно отправлен!', extra_tags='success')

            return redirect('cart')
