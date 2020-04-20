from django.contrib import admin
from django.urls import path, include
from shop import views

urlpatterns = [
    path('shopping-cart', views.cart, name='cart'),
    path('shopping-cart/<slug:slug>/add', views.add_travel_to_cart, name='add_travel_to_cart'),
    path('shopping-cart/<slug:slug>/remove', views.remove_travel_to_cart, name='remove_travel_to_cart'),
    path('checkout', views.checkout, name='checkout'),

]