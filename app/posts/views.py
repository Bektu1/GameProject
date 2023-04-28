from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product
from rest_framework import viewsets
from .serializers import ProductSerializer



class Product(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



