from django.contrib import admin
from django.urls import path
from app1.views import listado_productos, catalogo_tecnologia, vista_categorias, productos_por_subcategoria
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', listado_productos, name='home'),
    path('tecnologia/', catalogo_tecnologia, name='catalogo_tecnologia'),
    path('catalogo/<str:categoria_slug>/', vista_categorias, name='vista_categorias'),
    path('productos/<str:subcategoria_nombre>/', productos_por_subcategoria, name='productos_subcategoria'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
