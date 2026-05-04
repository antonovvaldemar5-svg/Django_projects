from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from .models import Product
from .forms import ProductForm
from .services import get_products_by_category

class HomeListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('catalog:product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {
        'form': form,
        'title': 'Создание продукта'
    })

def product_list(request):
    products = cache.get("all_products")
    if products is None:
        products = Product.objects.filter(is_published=True)
        cache.set("all_products", products, 3600)
    return render(request, 'catalog/product_list.html', {'products': products})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user and not request.user.has_perm('catalog.can_unpublish_product'):
        raise PermissionDenied
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

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user and not request.user.has_perm('catalog.can_unpublish_product'):
        raise PermissionDenied
    if request.method == 'POST':
        product.delete()
        return redirect('catalog:product_list')
    return render(request, 'catalog/product_confirm_delete.html', {
        'product': product
    })

@login_required
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not request.user.has_perm('catalog.can_unpublish_product'):
        raise PermissionDenied
    product.is_published = False
    product.save()
    return redirect('catalog:product_list')

def category_products(request, category_id):
    products = get_products_by_category(category_id)
    return render(request, "catalog/category_products.html", {"products": products})

