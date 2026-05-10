from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('Laptops', 'Laptops'),
        ('Componentes', 'Componentes'),
        ('Periféricos', 'Periféricos'),
        ('Accesorios', 'Accesorios'),
        ('GPUs', 'GPUs'),
        ('Monitores', 'Monitores'),
        ('Consolas', 'Consolas'),
        ('Auriculares', 'Auriculares'),
        ('Bocinas', 'Bocinas'),
        ('Headsets', 'Headsets'),
        ('Sistemas', 'Sistemas'),
        ('Smartwatches', 'Smartwatches'),
        ('Teléfonos', 'Teléfonos'),
        ('Tablets', 'Tablets'),
        ('Accesorios Inteligentes', 'Accesorios Inteligentes'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='images/')
    categoria = models.CharField(max_length=100, choices=CATEGORIAS)
    stock = models.IntegerField()
    
    def __str__(self):
        return self.nombre
