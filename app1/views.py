import boto3
import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from app1.models import Cliente, Producto, Pedido, DetallePedido
from app1.forms import InicioSesionForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password, check_password
import decimal
from decimal import Decimal

def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        contraseña = request.POST.get('password')


        if Cliente.objects.filter(email=email).exists():
            messages.error(request, f"El correo {email} ya se encuentra registrado.")
            return render(request, 'registro.html')

        try:
            nuevo_cliente = Cliente.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono,
                contraseña=make_password(contraseña)
            )
            id_generado = nuevo_cliente.id_cliente

            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            tabla = dynamodb.Table('registro_actividades')
            
            tabla.put_item(
                Item={
                    'userid': str(id_generado), 
                    'timestamp': int(time.time()),    
                    'evento': 'CLIENTE_REGISTRADO_AUTO',
                    'detalles': {
                        'nombre_registrado': nombre,
                        'email_contacto': email,
                        'metodo_registro': 'Auto-Increment RDS'
                    }
                }
            )

            messages.success(request, f"¡Éxito! Cliente registrado correctamente .")
            return redirect('iniciarSesion')
        
        except Exception as e:
            messages.error(request, f"Error en la operación: {e}")

    return render(request, 'registro.html')

def home(request):
    max_productos = 12
    productos = Producto.objects.all()[:max_productos]
    carousel_productos = productos[:8]
    return render(request, 'home.html', {
        'productos': productos,
        'carousel_productos': carousel_productos,
    })

from django.contrib.auth.hashers import check_password # IMPORTANTE

@csrf_protect
def iniciar_sesion(request):
    if request.method == 'POST':
        form = InicioSesionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password_ingresada = form.cleaned_data["contraseña"]

            try:
                # 1. Buscamos al cliente SOLO por email
                cliente = Cliente.objects.get(email=email)
                
                # 2. Comparamos la contraseña ingresada con el hash de la DB
                if check_password(password_ingresada, cliente.contraseña):
                    # ¡ÉXITO! Creamos la sesión
                    request.session['cliente_id'] = cliente.id_cliente
                    request.session['cliente_email'] = cliente.email
                    
                    # TIP DE SEGURIDAD: Nunca guardes la contraseña (ni el hash) en la sesión
                    # request.session['cliente_contraseña'] = cliente.contraseña <-- ELIMINAR ESTO
                    
                    messages.success(request, f"¡Bienvenido de nuevo, {cliente.nombre}!")
                    return redirect("home")
                else:
                    # Contraseña incorrecta
                    messages.error(request, "Correo o contraseña incorrectos.")
            
            except Cliente.DoesNotExist:
                # El correo no existe
                messages.error(request, "Correo o contraseña incorrectos.")
                
            return render(request, 'inicioSesion.html', {'form': form})
    else:
        form = InicioSesionForm()

    return render(request, 'inicioSesion.html', {'form': form})


def perfil(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('iniciarSesion')
    try:
        cliente = Cliente.objects.get(id_cliente=cliente_id)
        data = {'Cliente': cliente}
        return render(request, 'perfil.html', data)
    except Cliente.DoesNotExist:
        messages.error(request, "Cliente no encontrado.")
        return redirect('home')

def pedido(request):
    cliente_actual = request.user
    cliente_id_sesion = request.session.get('cliente_id')
    if not cliente_id_sesion:
        messages.error(request, "Debe iniciar sesión para realizar un pedido. ")
        return redirect('InicarSesion')

    if request.method == 'POST':
        ids_productos = request.POST.getlist('productos[]')

        if not ids_productos:
            messages.error(request, "El carrito de su compra se encuentra vacio. ")
            return redirect ('ver_carrito')
        
        try:
            with transaction.atomic():
                nuevo_pedido = Pedido.objects.create(id_cliente = cliente_actual, fecha = time.strftime('%Y-%m-%d %H:%M:%S'), estado = 'Procesando' )

                total_compra = 0
                nombre_productos = []

                for prod_id in ids_productos:
                 producto = Producto.objects.get(id_producto = prod_id )
                 DetallePedido.objects.create(
                    pedido=nuevo_pedido,
                    producto=producto,
                    cantidad=1
                )
                total_compra += producto.precio
                nombre_productos.append(producto.nombre)

            dynamodb = boto3.resource('dynamodb', region_name = 'us-east-1')
            tabla = dynamodb.Table('registro_actividades')

            tabla.put_item(
                Item={
                    'userid': str(cliente_actual.id),
                    'timestamp': int(time.time()),
                    'evento' : 'COMPRA_REALIZADA',
                    'detalles':{
                        'pedido_id': nuevo_pedido.id_pedido,
                        'monto_total': float(total_compra),
                        'items_comprados': nombre_productos,
                        'ip_origen': request.META.get('REMOTE_ADDR')

                    }

                }
            )

            messages.success(request, "Pedido #{nuevo_pedido.id_pedido} Realizado con éxito")
            return redirect('confirmacion_compra')
        except Exception as e:
            messages.error(request, "Error al procesar la compra: {e}")

    return render(request, 'realizar_pedido.html')

def listado_pedidos(request):
    cliente_id = request.session.get('cliente_id')
    if not cliente_id:
        return redirect('iniciarSesion')
    try:
        cliente = Cliente.objects.get(id_cliente=cliente_id)
        pedidos = Pedido.objects.filter(id_cliente=cliente).order_by('-fecha')
        return render(request, 'listado_pedidos.html', {'pedidos': pedidos, 'Cliente': cliente})
    except Cliente.DoesNotExist:
        messages.error(request, "Cliente no encontrado.")
        return redirect('iniciarSesion')


def salir(request):
    request.session.flush()
    return redirect('iniciarSesion')

def carrito(request):
    carrito_session = request.session.get('carrito', {})
    carrito_items = []
    total = 0
    
    for producto_id, cantidad in carrito_session.items():
        try:
            producto = Producto.objects.get(id_producto=int(producto_id))
            subtotal = producto.precio_producto * cantidad
            carrito_items.append({
                'id': producto.id_producto,
                'nombre': producto.nombre_producto,
                'precio': producto.precio_producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal
        except Producto.DoesNotExist:
            pass
    
    return render(request, 'carrito.html', {'carrito': carrito_items, 'total': total})

def agregar_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)
    
    if producto_id_str in carrito:
        carrito[producto_id_str] += 1
    else:
        carrito[producto_id_str] = 1
    
    request.session['carrito'] = carrito
    request.session.modified = True
    
    messages.success(request, f"Producto agregado al carrito correctamente.")
    return redirect('carrito')

def checkout(request):
    cliente_id = request.session.get('cliente_id')
    carrito_session = request.session.get('carrito', {})
    
    if not carrito_session:
        messages.error(request, "El carrito está vacío.")
        return redirect('carrito')
    
    carrito_items = []
    subtotal = 0
    
    for producto_id, cantidad in carrito_session.items():
        try:
            producto = Producto.objects.get(id_producto=int(producto_id))
            item_subtotal = float(producto.precio_producto) * cantidad
            carrito_items.append({
                'id': producto.id_producto,
                'nombre': producto.nombre_producto,
                'precio': producto.precio_producto,
                'cantidad': cantidad,
                'subtotal': f"${item_subtotal:,.2f}".replace(',', '.')
            })
            subtotal += item_subtotal
        except Producto.DoesNotExist:
            pass
    
    # Cálculo de impuesto y total
    envio = 10000
    impuesto = subtotal * 0.19
    total = subtotal + envio + impuesto
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        region = request.POST.get('region')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        codigo_postal = request.POST.get('codigo_postal')
        metodo_pago = request.POST.get('metodo_pago')
        terminos = request.POST.get('terminos')
        
        if not terminos:
            messages.error(request, "Debes aceptar los términos y condiciones.")
            return render(request, 'checkout.html', {
                'carrito': carrito_items,
                'subtotal': f"${subtotal:,.2f}".replace(',', '.'),
                'impuesto': f"${impuesto:,.2f}".replace(',', '.'),
                'total': f"${total:,.2f}".replace(',', '.')
            })
        
        try:
            with transaction.atomic():
                # Crear pedido
                nuevo_pedido = Pedido.objects.create(
                    id_cliente_id=cliente_id,
                    fecha=time.strftime('%Y-%m-%d %H:%M:%S'),
                    estado='Procesando'
                )
                
                # Crear detalles del pedido
                for producto_id, cantidad in carrito_session.items():
                    producto = Producto.objects.get(id_producto=int(producto_id))
                    DetallePedido.objects.create(
                        pedido=nuevo_pedido,
                        producto=producto,
                        cantidad=cantidad
                    )
                
                # Registrar en DynamoDB
                dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
                tabla = dynamodb.Table('registro_actividades')
                
                tabla.put_item(
                    Item={
                        'userid': str(cliente_id),
                        'timestamp': int(time.time()),
                        'evento': 'PAGO_REALIZADO',
                        'detalles': {
                            'pedido_id': nuevo_pedido.pedido_id,
                            'monto_total': Decimal(str(total)),
                            'metodo_pago': metodo_pago,
                            'cliente_email': email,
                            'direccion_envio': f"{direccion}, {ciudad}, {region}",
                            'ip_origen': request.META.get('REMOTE_ADDR')
                        }
                    }
                )
                
                # Limpiar carrito
                request.session['carrito'] = {}
                request.session.modified = True
                
                messages.success(request, f"¡Pago realizado exitosamente! Pedido #{nuevo_pedido.pedido_id}")
                return redirect('confirmacion_compra')
        
        except Exception as e:
            messages.error(request, f"Error al procesar el pago: {str(e)}")
            return render(request, 'checkout.html', {
                'carrito': carrito_items,
                'subtotal': f"${subtotal:,.2f}".replace(',', '.'),
                'impuesto': f"${impuesto:,.2f}".replace(',', '.'),
                'total': f"${total:,.2f}".replace(',', '.')
            })
    
    return render(request, 'checkout.html', {
        'carrito': carrito_items,
        'subtotal': f"${subtotal:,.2f}".replace(',', '.'),
        'impuesto': f"${impuesto:,.2f}".replace(',', '.'),
        'total': f"${total:,.2f}".replace(',', '.')
    })

def confirmacion_compra(request):
    return render(request, 'confirmacion_compra.html')
