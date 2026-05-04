from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('list/', views.product_list, name='product_list'),
    path('contacts/', views.ContactsTemplateView.as_view(), name='contacts'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('unpublish/<int:pk>/', views.unpublish_product, name='unpublish'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
]