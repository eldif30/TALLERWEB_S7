from itertools import groupby
from operator import attrgetter
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm, TipoProductoForm
from .models import Producto, TipoProducto, Pedido
from aplicaciones.producto.models import Producto
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mensaje

# Create your views here.

"""
Vamos a migrar las vistas basadas en funciones por vistas basadas
en clase para aprovechar al maximo lo que el framework nos ofrece

"""

# Vista basada en el template view para renderizar el template con el
# contexto de la vista


@method_decorator(login_required, name='dispatch')
class InicioView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filtrar solo productos disponibles y ordenarlos por tipo y nombre
        productos = Producto.objects.filter(disponible=True).order_by('tipo', 'nombre')
        # Agrupar los productos por tipo
        grouped_productos = groupby(productos, key=attrgetter('tipo'))
        # Crear un diccionario con tipo como clave y productos como valores
        context['productos_por_tipo'] = {
            tipo: list(items) for tipo, items in grouped_productos
        }
        return context


@method_decorator(login_required, name='dispatch')
class CrearProductoView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/crear_producto.html'
    success_url = reverse_lazy('producto:listar_producto')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'titulo': 'crear producto',
                                                    'form': self.form_class})


@method_decorator(login_required, name='dispatch')
class EliminarProductoView(DeleteView):
    model = Producto
    success_url = reverse_lazy('producto:listar_producto')


@method_decorator(login_required, name='dispatch')
class EliminarPedidoView(DeleteView):
    model = Pedido
    success_url = reverse_lazy('producto:pedidos')

# Vista basa en ListView para mostrar informacion de la base de datos
# en templates


@method_decorator(login_required, name='dispatch')
class ListarProductoView(ListView):
    model = Producto
    template_name = 'producto/listar_producto.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos'] = TipoProducto.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        # Iterar sobre los productos y guardar los cambios
        for producto in Producto.objects.all():
            if f"guardar_{producto.codigo}" in request.POST:
                producto.nombre = request.POST.get(f"nombre_{producto.codigo}")
                producto.tipo_id = request.POST.get(f"tipo_{producto.codigo}")
                producto.descripcion = request.POST.get(f"descripcion_{producto.codigo}")
                producto.precio = request.POST.get(f"precio_{producto.codigo}")
                producto.disponible = f"disponible_{producto.codigo}" in request.POST

                if f"imagen_{producto.codigo}" in request.FILES:
                    producto.imagen = request.FILES[f"imagen_{producto.codigo}"]

                producto.save()
                break  # Solo guardamos el producto que corresponde al botón presionado

        return redirect('producto:listar_producto')


# eliminación directa

@login_required()
def eliminar_producto(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    producto.delete()
    return redirect('producto:listar_producto')


@method_decorator(login_required, name='dispatch')
class EditarProductoView(UpdateView):
    model = Producto
    template_name = 'producto/editar_producto.html'
    # Se utiliza un formulario para que se envie al template
    # form_class = ProductoForm
    # Se define la accion que el va a realizar una vez haga el proceso
    success_url = reverse_lazy('producto:listar_producto')

@method_decorator(login_required, name='dispatch')
class EditarPedidoView(UpdateView):
    model = Pedido
    template_name = 'producto/editar_pedido.html'
    # Se utiliza un formulario para que se envie al template
    # form_class = PedidoForm
    # Se define la accion que el va a realizar una vez haga el proceso
    success_url = reverse_lazy('producto:pedido')


class CrearTipoView(CreateView):
    tipo = TipoProducto
    form_class = TipoProductoForm
    template_name = 'producto/crear_tipo.html'
    success_url = reverse_lazy('index')

@method_decorator(login_required, name='dispatch')
class MenuView(ListView):
    model = Producto
    template_name = 'producto/menu.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filtrar solo productos disponibles y ordenarlos por tipo y nombre
        productos = Producto.objects.filter(disponible=True).order_by('tipo', 'nombre')
        # Agrupar los productos por tipo
        grouped_productos = groupby(productos, key=attrgetter('tipo'))
        # Crear un diccionario con tipo como clave y productos como valores
        context['productos_por_tipo'] = {
            tipo: list(items) for tipo, items in grouped_productos
        }
        return context


# Vista para Seguimiento
@method_decorator(login_required, name='dispatch')
class SeguimientoView(TemplateView):
    template_name = 'producto/seguimiento.html'

# Vista para GPS
@method_decorator(login_required, name='dispatch')
class GPSView(TemplateView):
    template_name = 'producto/gps.html'

@login_required
def crear_pedido(request):
    if request.method == 'POST':
        productos_ids = request.POST.getlist('productos')
        direccion_destino = request.POST.get('direccion_destino')

        # Crear el pedido
        pedido = Pedido.objects.create(direccion_destino=direccion_destino)
        productos = Producto.objects.filter(codigo__in=productos_ids)
        pedido.productos.set(productos)
        pedido.calcular_total()  # Calcular el total basado en los productos
        return redirect('producto:pedidos')

    productos = Producto.objects.filter(disponible=True)
    return render(request, 'producto/crear_pedido.html', {'productos': productos})



@method_decorator(login_required, name='dispatch')
class ListarPedidoView(ListView):
    model = Pedido
    template_name = 'producto/pedidos.html'
    context_object_name = 'pedidos'

    def post(self, request, *args, **kwargs):
        # Iterar sobre los productos y guardar los cambios
        for pedido in Pedido.objects.all():
            if f"guardar_{pedido.id}" in request.POST:
                pedido.repartidor = request.POST.get(f"repartidor")
                pedido.estado = request.POST.get(f"estado")
                
                pedido.save()
                break  # Solo guardamos el producto que corresponde al botón presionado

        return redirect('producto:pedidos')

@login_required
def eliminar_pedido(request, id):
    pedido = Pedido.objects.get(id=id)
    pedido.delete()
    return redirect('producto:pedidos')

@login_required
def chat_view(request):
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            Mensaje.objects.create(usuario=request.user, contenido=contenido)
        return redirect('producto:chat')  # Redirige para evitar reenvíos al recargar la página

    mensajes = Mensaje.objects.all().order_by('-fecha_creacion')[:50]  # Últimos 50 mensajes
    return render(request, 'producto/chat.html', {'mensajes': mensajes})