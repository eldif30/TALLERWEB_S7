from django.urls import path
from .views import chat_view, CrearProductoView, ListarProductoView, EliminarPedidoView, EditarProductoView, EditarPedidoView, EliminarProductoView, CrearTipoView, GPSView, crear_pedido, ListarPedidoView


# Creación de los paths
urlpatterns = [
    path('crear_producto', CrearProductoView.as_view(), name='crear_producto'),
    path('listar_producto', ListarProductoView.as_view(), name='listar_producto'),
    path('editar_producto/<int:pk>',
         EditarProductoView.as_view(), name='editar_producto'),
    path('eliminar_producto/<int:pk>',
         EliminarProductoView.as_view(), name='eliminar_producto'),
    path('crear_tipo', CrearTipoView.as_view(), name='crear_tipo'),
    path('gps/', GPSView.as_view(), name='gps'),
    path('crear_pedido/', crear_pedido, name='crear_pedido'),
    path('pedidos/', ListarPedidoView.as_view(), name='pedidos'),
    path('eliminar_pedido/<int:pk>',
         EliminarPedidoView.as_view(), name='eliminar_pedido'),
     path('editar_pedido/<int:pk>',
         EditarPedidoView.as_view(), name='editar_pedido'),
     path('chat/', chat_view, name='chat'),

]
