from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='post'),
    path('home', views.home, name='home'),
    path('uploadProduct', views.uploadProduct, name='uploadProduct'),
    path('myListings', views.myListings, name='listmyListings'),
    path('myCart', views.listAllMyCart, name='listMyCart'),
    path('purchaseHistory', views.displayHistory, name='listOrderHistory'),
    # STRIPE API
    path('myCart', views.payCart, name='payCart'),
]
