from django.contrib import admin
from django.urls import path, include
from travels import views

urlpatterns = [
    path('', views.travels, name='travels'),
    path('<slug:slug>', views.travel, name='travel'),
]