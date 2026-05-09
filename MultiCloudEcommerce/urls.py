"""
URL configuration for MultiCloudEcommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1.views import listado_productos, catalogo_ropa, catalogo_tecnologia, catalogo_hogar, catalogo_categoria
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', listado_productos, name='home'),
    path('ropa/', catalogo_ropa, name='catalogo_ropa'),
    path('tecnologia/', catalogo_tecnologia, name='catalogo_tecnologia'),
    path('hogar/', catalogo_hogar, name='catalogo_hogar'),
    path('categoria/<slug:slug>/', catalogo_categoria, name='catalogo_categoria'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
