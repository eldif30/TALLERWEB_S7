from django import forms as fm
from .models import TipoProducto, Producto

# Formulario del tipo de producto
class TipoProductoForm(fm.ModelForm):
    class Meta:
        model = TipoProducto
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre del nuevo tipo'
        }
        widgets = {
            'nombre': fm.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre del tipo de producto'
                }
            )
        }

# Formulario del producto
class ProductoForm(fm.ModelForm):  # Cambiado forms.ModelForm por fm.ModelForm
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'descripcion', 'precio', 'disponible', 'imagen', 'tipo']
        labels = {
            'codigo': 'Código del producto',
            'nombre': 'Nombre del plato',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'disponible': '¿Está disponible?',
            'imagen': 'Imagen del plato',
            'tipo': 'Categoría',
        }
        widgets = {
            'codigo': fm.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el código del producto'
            }),
            'nombre': fm.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto'
            }),
            'descripcion': fm.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción del producto'
            }),
            'precio': fm.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el precio del producto'
            }),
            'disponible': fm.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'imagen': fm.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'tipo': fm.Select(attrs={
                'class': 'form-control'
            }),
        }
