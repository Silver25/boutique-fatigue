# from django.contrib import admin - removed because didn't used
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
]
