from django.shortcuts import render
from app1.models import Producto


def listado_productos(request):
    max_productos = 12
    productos = Producto.objects.all()[:max_productos]
    carousel_productos = productos[:8]
    return render(request, 'lista_productos.html', {
        'productos': productos,
        'carousel_productos': carousel_productos,
    })


def catalogo_tecnologia(request):
    subcategorias = [
        {'nombre': 'Computación', 'descripcion': 'Laptops, accesorios y componentes para trabajar y estudiar.'},
        {'nombre': 'Audio', 'descripcion': 'Auriculares, bocinas y soluciones de sonido para el día a día.'},
        {'nombre': 'Gaming', 'descripcion': 'Hardware y periféricos para gaming a otro nivel.'},
        {'nombre': 'Gadgets', 'descripcion': 'Dispositivos inteligentes y chucherías tecnológicas.'},
    ]
    return render(request, 'catalogo_tecnologia.html', {'subcategorias': subcategorias})

def vista_categorias(request, categoria_slug):
    template_name = f'catalogo_{categoria_slug}.html'
    return render(request, template_name, {
        'categoria': categoria_slug.capitalize()
    })

def productos_por_subcategoria(request, subcategoria_nombre):
    productos = Producto.objects.filter(categoria__iexact=subcategoria_nombre)
    return render(request, 'productos_subcategoria.html', {
        'productos': productos,
        'subcategoria': subcategoria_nombre
    })
