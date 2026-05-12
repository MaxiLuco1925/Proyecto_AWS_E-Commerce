<<<<<<< HEAD
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
=======
from django.urls import path
from app1.views import home, registro, iniciar_sesion, perfil, listado_pedidos, salir, carrito, agregar_carrito, checkout, confirmacion_compra
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro/', registro, name='registro'),
    path('iniciar-sesion/', iniciar_sesion, name='iniciarSesion'),
    path('perfil/', perfil, name='perfil'),
    path('listado-pedidos/', listado_pedidos, name='listado_pedidos'),
    path('carrito/', carrito, name='carrito'),
    path('agregar-carrito/<int:producto_id>/', agregar_carrito, name='agregar_carrito'),
    path('checkout/', checkout, name='checkout'),
    path('confirmacion-compra/', confirmacion_compra, name='confirmacion_compra'),
    path('', home, name='home'),
    path('salir/', salir, name='salir'),

]
>>>>>>> 7d890b7 (Avance final)
