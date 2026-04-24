from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product
from django.urls import reverse
from .forms import ProductForm

class HomeListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ContactsTemplateView(TemplateView):
    model = Product
    template_name = "catalog/contacts.html"


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_list')
    else:
        form = ProductForm()

    return render(request, 'catalog/product_form.html', {
        'form': form,
        'title': 'Создание продукта'
    })


def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {
        'products': products
    })


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'catalog/product_form.html', {
        'form': form,
        'title': 'Редактирование продукта'
    })


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('catalog:product_list')

    return render(request, 'catalog/product_confirm_delete.html', {
        'product': product
    })



