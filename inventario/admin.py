from django.contrib import admin
from .models import Producto, Categoria, Cliente, Sale, SaleItem

# --------------------------
# ADMIN PRODUCTO
# --------------------------
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'categoria', 'stock', 'precio_compra', 'precio_venta', 'ganancia_total')
    search_fields = ('nombre', 'marca')
    list_filter = ('categoria',)

    readonly_fields = ('vendidos',)  # opcional: campos que no quieres editar desde admin

    def ganancia_total(self, obj):
        """
        Calcula la ganancia total aproximada según stock y precios
        """
        return (obj.precio_venta - obj.precio_compra) * obj.stock
    ganancia_total.short_description = 'Ganancia Total'

# --------------------------
# ADMIN CATEGORIA
# --------------------------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# --------------------------
# ADMIN CLIENTE
# --------------------------
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento')
    search_fields = ('nombre', 'documento')

# --------------------------
# INLINE PARA ITEMS DE VENTA
# --------------------------
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    readonly_fields = ('precio', 'subtotal')  # no se puede modificar precio desde el inline

    def subtotal(self, obj):
        return obj.cantidad * obj.precio
    subtotal.short_description = "Subtotal"

# --------------------------
# ADMIN SALE
# --------------------------
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tipo_comprobante', 'fecha', 'total_venta')
    list_filter = ('tipo_comprobante', 'fecha')
    search_fields = ('cliente__nombre',)
    inlines = [SaleItemInline]

    def total_venta(self, obj):
        return sum(item.cantidad * item.precio for item in obj.items.all())
    total_venta.short_description = "Total Venta"

# --------------------------
# ADMIN SALE ITEM
# --------------------------
@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'producto', 'cantidad', 'precio', 'subtotal')
    search_fields = ('producto__nombre',)

    def subtotal(self, obj):
        return obj.cantidad * obj.precio
    subtotal.short_description = "Subtotal"
