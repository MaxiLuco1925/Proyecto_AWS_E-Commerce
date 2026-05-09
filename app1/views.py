from django.http import Http404
from django.shortcuts import render
from app1.models import Producto


# Create your views here.

def listado_productos(request):
    max_productos = 12
    productos = Producto.objects.all()[:max_productos]
    carousel_productos = productos[:8]
    categorias = [
        {'id': 'ropa', 'nombre': 'Ropa', 'icono': 'fa-tshirt'},
        {'id': 'tecnologia', 'nombre': 'Tecnología', 'icono': 'fa-laptop'},
        {'id': 'hogar', 'nombre': 'Hogar', 'icono': 'fa-home'},
        {'id': 'deporte', 'nombre': 'Deporte', 'icono': 'fa-basketball-ball'},
        {'id': 'belleza', 'nombre': 'Belleza', 'icono': 'fa-spa'},
        {'id': 'mascotas', 'nombre': 'Mascotas', 'icono': 'fa-paw'},
        {'id': 'juguetes', 'nombre': 'Juguetes', 'icono': 'fa-gamepad'},
        {'id': 'libros', 'nombre': 'Libros', 'icono': 'fa-book'},
    ]
    return render(request, 'lista_productos.html', {
        'productos': productos,
        'carousel_productos': carousel_productos,
        'categorias': categorias,
    })


def catalogo_ropa(request):
    subcategorias = [
        {'nombre': 'Casual', 'descripcion': 'Ropa cómoda para el día a día.'},
        {'nombre': 'Formal', 'descripcion': 'Prendas elegantes para oficina y ocasiones serias.'},
        {'nombre': 'Evento', 'descripcion': 'Looks especiales para celebraciones y fiestas.'},
        {'nombre': 'Deportiva', 'descripcion': 'Conjuntos activos para entrenar y moverte con estilo.'},
    ]
    return render(request, 'catalogo_ropa.html', {'subcategorias': subcategorias})


def catalogo_tecnologia(request):
    subcategorias = [
        {'nombre': 'Computación', 'descripcion': 'Laptops, accesorios y componentes para trabajar y estudiar.'},
        {'nombre': 'Audio', 'descripcion': 'Auriculares, bocinas y soluciones de sonido para el día a día.'},
        {'nombre': 'Gaming', 'descripcion': 'Hardware y periféricos para gaming a otro nivel.'},
    ]
    return render(request, 'catalogo_tecnologia.html', {'subcategorias': subcategorias})


def catalogo_hogar(request):
    subcategorias = [
        {'nombre': 'Decoración', 'descripcion': 'Ideas y accesorios para embellecer cada rincón del hogar.'},
        {'nombre': 'Cocina', 'descripcion': 'Utensilios, electrodomésticos y menaje funcional.'},
        {'nombre': 'Muebles', 'descripcion': 'Soluciones cómodas y elegantes para sala, comedor y dormitorio.'},
        {'nombre': 'Jardín', 'descripcion': 'Todo para el exterior, plantas, herramientas y relax al aire libre.'},
        {'nombre': 'Smart home', 'descripcion': 'Sistemas y accesorios para mantener tu hogar inteligente.'},
    ]
    return render(request, 'catalogo_Hogar.html', {'subcategorias': subcategorias})


def catalogo_categoria(request, slug):
    categorias = {
        'ropa': {
            'template': 'catalogo_ropa.html',
            'title': 'Catálogo de Ropa',
            'description': 'Encuentra estilos casual, formal, de evento y deportiva para cada ocasión.',
            'subcategorias': [
                {'nombre': 'Casual', 'descripcion': 'Ropa cómoda para el día a día.'},
                {'nombre': 'Formal', 'descripcion': 'Prendas elegantes para oficina y ocasiones serias.'},
                {'nombre': 'Evento', 'descripcion': 'Looks especiales para celebraciones y fiestas.'},
                {'nombre': 'Deportiva', 'descripcion': 'Conjuntos activos para entrenar y moverte con estilo.'},
            ],
        },
        'tecnologia': {
            'template': 'catalogo_tecnologia.html',
            'title': 'Catálogo de Tecnología',
            'description': 'Explora gadgets, audio, gaming y computación en un solo lugar.',
            'subcategorias': [
                {'nombre': 'Computación', 'descripcion': 'Laptops, accesorios y componentes para trabajar y estudiar.'},
                {'nombre': 'Audio', 'descripcion': 'Auriculares, bocinas y soluciones de sonido para el día a día.'},
                {'nombre': 'Gaming', 'descripcion': 'Hardware y periféricos para gaming a otro nivel.'},
                {'nombre': 'Gadgets', 'descripcion': 'Dispositivos inteligentes y chucherías tecnológicas.'},
            ],
        },
        'hogar': {
            'template': 'catalogo_Hogar.html',
            'title': 'Catálogo de Hogar',
            'description': 'Elige la sección para mejorar tu casa con estilo y funcionalidad.',
            'subcategorias': [
                {'nombre': 'Decoración', 'descripcion': 'Ideas y accesorios para embellecer cada rincón del hogar.'},
                {'nombre': 'Cocina', 'descripcion': 'Utensilios, electrodomésticos y menaje funcional.'},
                {'nombre': 'Muebles', 'descripcion': 'Soluciones cómodas y elegantes para sala, comedor y dormitorio.'},
                {'nombre': 'Jardín', 'descripcion': 'Todo para el exterior, plantas, herramientas y relax al aire libre.'},
                {'nombre': 'Smart home', 'descripcion': 'Sistemas y accesorios para mantener tu hogar inteligente.'},
            ],
        },
        'deporte': {
            'template': 'catalogo_deporte.html',
            'title': 'Catálogo de Deporte',
            'description': 'Ropa, calzado y equipo para entrenar con comodidad y estilo.',
            'subcategorias': [
                {'nombre': 'Fitness', 'descripcion': 'Ropa y accesorios para gimnasio y entrenamiento.'},
                {'nombre': 'Running', 'descripcion': 'Zapatillas, ropa y gadgets para correr mejor.'},
                {'nombre': 'Outdoor', 'descripcion': 'Equipo para actividades al aire libre y deportes de aventura.'},
                {'nombre': 'Yoga', 'descripcion': 'Mats, ropa cómoda y accesorios para practicar yoga.'},
            ],
        },
        'belleza': {
            'template': 'catalogo_belleza.html',
            'title': 'Catálogo de Belleza',
            'description': 'Cuidados y productos para que te veas y te sientas bien.',
            'subcategorias': [
                {'nombre': 'Maquillaje', 'descripcion': 'Cosmética para un look impecable.'},
                {'nombre': 'Cuidado facial', 'descripcion': 'Rutinas y productos para una piel radiante.'},
                {'nombre': 'Perfumes', 'descripcion': 'Aromas para cada estilo y ocasión.'},
                {'nombre': 'Cuidado corporal', 'descripcion': 'Hidratación, spa y bienestar en casa.'},
            ],
        },
        'mascotas': {
            'template': 'catalogo_mascotas.html',
            'title': 'Catálogo de Mascotas',
            'description': 'Todo para el cuidado, juego y comodidad de tu mascota.',
            'subcategorias': [
                {'nombre': 'Alimentos', 'descripcion': 'Comida balanceada para perros, gatos y pequeñas mascotas.'},
                {'nombre': 'Juguetes', 'descripcion': 'Diversión y estimulación para tu mascota.'},
                {'nombre': 'Higiene', 'descripcion': 'Accesorios para baño, cepillado y limpieza.'},
                {'nombre': 'Camas y casas', 'descripcion': 'Espacios cómodos para descansar.'},
            ],
        },
        'juguetes': {
            'template': 'catalogo_juguetes.html',
            'title': 'Catálogo de Juguetes',
            'description': 'Opciones divertidas para niños y niñas de todas las edades.',
            'subcategorias': [
                {'nombre': 'Educativos', 'descripcion': 'Juguetes que estimulan aprendizaje y creatividad.'},
                {'nombre': 'Figuras', 'descripcion': 'Coleccionables, figuras de acción y muñecos.'},
                {'nombre': 'Juegos de mesa', 'descripcion': 'Diversión familiar garantizada.'},
                {'nombre': 'Construcción', 'descripcion': 'Bloques y sets para construir y crear.'},
            ],
        },
        'libros': {
            'template': 'catalogo_libros.html',
            'title': 'Catálogo de Libros',
            'description': 'Encuentra lecturas para todos los gustos y edades.',
            'subcategorias': [
                {'nombre': 'Ficción', 'descripcion': 'Novelas y relatos para perderte en nuevas historias.'},
                {'nombre': 'No ficción', 'descripcion': 'Ensayos, biografías y libros de conocimiento.'},
                {'nombre': 'Infantil', 'descripcion': 'Cuentos y libros ilustrados para los más pequeños.'},
                {'nombre': 'Autoayuda', 'descripcion': 'Guías para mejorar hábitos y bienestar personal.'},
            ],
        },
    }
    categoria = categorias.get(slug)
    if not categoria:
        raise Http404('Categoría no encontrada')
    return render(request, categoria['template'], {
        'category_title': categoria['title'],
        'category_description': categoria['description'],
        'subcategorias': categoria['subcategorias'],
    })

