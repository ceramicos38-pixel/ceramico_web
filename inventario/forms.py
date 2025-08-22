from django import forms
from .models import Producto, Categoria, Cliente, Sale, SaleItem
from decimal import Decimal

# --------------------------
# FORMULARIO PRODUCTO
# --------------------------
class ProductoForm(forms.ModelForm):
    nueva_categoria = forms.CharField(
        max_length=120,
        required=False,
        label="Nueva Categoría",
        help_text="Escribe un nombre si quieres crear una categoría nueva"
    )

    class Meta:
        model = Producto
        fields = [
            'nombre',
            'marca',
            'categoria',
            'nueva_categoria',  # NUEVO CAMPO
            'stock',
            'unidad_medida',
            'precio_compra',
            'porcentaje_ganancia',
            'vendidos',
            'proveedor',
        ]

# --------------------------
# FORMULARIO VENTA
# --------------------------
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['cliente', 'tipo_comprobante']  # el total se calcula solo

# --------------------------
# FORMULARIO ITEM DE VENTA
# --------------------------
class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['producto', 'cantidad', 'precio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mostrar nombre, marca, stock y precio de venta
        self.fields['producto'].queryset = Producto.objects.all()
        self.fields['producto'].label_from_instance = (
            lambda obj: f"{obj.nombre} | {obj.marca} | Stock: {obj.stock} | Precio: {obj.precio_venta}"
        )

        # Precio editable
        self.fields['precio'].widget.attrs.update({
            'class': 'form-control',
            'step': '0.01'
        })

        # Cantidad editable
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})

# inventario/forms.py

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nueva categoría'}),
        }
