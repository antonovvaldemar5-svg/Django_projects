from django.shortcuts import render
from django.template.context_processors import request
from .models import Product


def home(request):
    products = Product.objects.all()
    return render(request, "catalog/home.html")

def contacts(request):
    return render(request, "catalog/contacts.html")

def product_detail(request):
    return render(request, "catalog/product_detail.html")

