from django.db import models

# Create your models here.
class Pedidos(models.Model):
    ESTADOS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]

    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('clientes.Clientes', on_delete=models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='pendiente')


# Modelo de detalle pedido
class DetallePedido(models.Model):
    id = models.AutoField(primary_key=True)
    # Llaves foraneas del pedido y del producto
    pedido_id = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    producto_id = models.ForeignKey('productos.Productos', on_delete=models.CASCADE)
    
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)