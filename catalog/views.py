from django.shortcuts import render
from django.template.context_processors import request


def home(request):
    return render(request, "catalog/home.html")

def contacts(request):
    return render(request, "catalog/contacts.html")
