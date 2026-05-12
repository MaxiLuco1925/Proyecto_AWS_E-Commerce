from django.db import models



class Cliente(models.Model):
    id_cliente = models.AutoField(db_column='ID_CLIENTE', primary_key=True) 
    nombre = models.CharField(db_column='NOMBRE', max_length=40, blank=True, null=True)  
    email = models.CharField(db_column='EMAIL', max_length=60, null=True)  
    telefono = models.CharField(db_column='TELEFONO', max_length=30, blank=True, null=True)  
    contraseña = models.CharField(db_column='CONTRASEÑA',max_length=256)


    class Meta:
        managed = True
        db_table = 'CLIENTE'





class Pedido(models.Model):
    pedido_id = models.AutoField(db_column='PEDIDO_ID', primary_key=True)  
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='ID_CLIENTE', blank=True, null=True)  
    fecha = models.DateTimeField(db_column='FECHA', blank=True, null=True)  
    estado = models.CharField(db_column='ESTADO', max_length=30, blank=True, null=True, default='Procesando')  

    class Meta:
        managed = True
        db_table = 'PEDIDO'


class Producto(models.Model):
    id_producto = models.AutoField(db_column='ID_PRODUCTO', primary_key=True)
    nombre_producto = models.CharField(db_column='NOMBRE_PRODUCTO', max_length=30, blank=True, null=True)
    precio_producto = models.DecimalField(db_column='PRECIO_PRODUCTO', max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'PRODUCTO'

class DetallePedido(models.Model):
    id_detalle_pedido = models.AutoField(db_column='ID_DETALLE_PEDIDO', primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, db_column='ID_PEDIDO')
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, db_column='ID_PRODUCTO', null=True, blank=True)
    cantidad = models.IntegerField(db_column='CANTIDAD', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'DETALLE_PEDIDO'






