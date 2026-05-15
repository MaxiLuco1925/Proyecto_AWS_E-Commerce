
from django.urls import path
from app1.views import home, registro, iniciar_sesion, perfil, listado_pedidos, salir, carrito, agregar_carrito, checkout, confirmacion_compra, panel_admin, listausuarios, listadoProductos, gestionarPedidoAdmin, perfilAdministrador, ver_dynamodb
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
    path('admin_nexcor/', panel_admin, name= 'panel_admin'),
    path ('listado_usuarios/', listausuarios, name = 'listado_clientes'),
    path('inventario/', listadoProductos, name= 'productos'),
    path('gestionar-pedido/<int:pedido_id>/',gestionarPedidoAdmin, name='gestionar_pedido'),
    path('perfil_administrador/', perfilAdministrador, name = 'perfilAdmin' ),
    path('eventos/', ver_dynamodb, name='ver_dynamodb')
]

