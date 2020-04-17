from django.contrib import admin
from django.urls import path, include
from shop import views

urlpatterns = [
    path('shopping-cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
]