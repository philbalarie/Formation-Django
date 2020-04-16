from django.contrib import admin
from django.urls import path, include
from travels import views

urlpatterns = [
    path('travels', views.travels, name='travels')
]