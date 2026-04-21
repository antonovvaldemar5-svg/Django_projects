from django.contrib import admin
from django.urls import path, include
from django.utils.translation.trans_real import catalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('blogs/', include("blog.urls", namespace="blog"))
]

