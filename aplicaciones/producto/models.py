from django.db import models
from django.conf import settings  

# Create your models here.

# Modelo tipo de producto


class TipoProducto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=150, null=False, blank=False, unique=True)

    def __str__(self):
        return "{}".format(self.nombre)


# Modelo Producto (Plato del menú)
class Producto(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False, unique=True)
    descripcion = models.TextField(null=True, blank=True)  # Detalles del plato
    precio = models.IntegerField()  # Precio del plato en valores enteros
    disponible = models.BooleanField(default=True)  # Estado de disponibilidad
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)  # Imagen del plato
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)  # Relación con el tipo de producto
    fecha_creacion = models.DateField('Fecha de creación', auto_now=True)

    def __str__(self):
        return f"codigo: {self.codigo} nombre: {self.nombre} tipo: {self.tipo} precio: {self.precio} disponible: {self.disponible}"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('asignado', 'Asignado'),
        ('en_proceso', 'En Proceso'),
        ('entregado', 'Entregado'),
    ]

    productos = models.ManyToManyField(Producto)  # Relación con productos
    direccion_origen = models.CharField(max_length=255, null=True, blank=True)
    direccion_destino = models.CharField(max_length=255)
    repartidor = models.CharField(max_length=150, null=True, blank=True)  # Repartidor asignado
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Total del pedido
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del pedido

    def calcular_total(self):
        """
        Calcula el total del pedido basado en los precios de los productos.
        """
        total = sum(producto.precio for producto in self.productos.all())
        self.total = total
        self.save()

    def __str__(self):
        return f"Pedido #{self.id} - Estado: {self.estado}"
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['estado']


class Mensaje(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Cambia auth.User a settings.AUTH_USER_MODEL
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario}: {self.contenido[:50]}"

