"""food_delivery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import base, product, addCard, cart, removeCart, about, search, signin, signup, signout
from food_delivery.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
    path('', base, name='base'),
    # path('test/<int:id>', test, name='test'),
    path('product/<int:id>', product, name='product'),
    path('addCard/<int:pk>', addCard, name='addCard'),
    path('cart', cart, name='cart'),
    path('about', about, name='about'),
    path('search', search, name='search'),
    path('removeCart/<int:id>', removeCart, name='removeCart'),
    path('signup', signup, name='signup'),
    path('signin', signin, name='signin'),
    path('signout', signout, name='signout'),
    path('admin/', admin.site.urls),
]


urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)