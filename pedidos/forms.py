
from django import forms

from clientes.models import Clientes
from pedidos.models import DetallePedido, Pedidos


class PedidosForm(forms.ModelForm):
    class Meta:
        # Especificamos el modelo y los campos a incluir en el formulario
        model = Pedidos
        fields = ['cliente', 'fecha', 'estado']

        # Inputs y clases CSS
        widgets = {
            'cliente': forms.Select(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400'}),
            'fecha': forms.DateInput(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Para que el select no tenga ---
        self.fields['cliente'].empty_label = None
            
    # Para validar la fecha
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        # Si la fecha está vacía
        if fecha is None:
            raise forms.ValidationError('La fecha no puede estar vacia')

        return fecha

# Form de producto y cantidad del pedido
class DetallePedidoForm(forms.ModelForm):
    class Meta:
        # Especificamos el modelo y los campos a incluir en el formulario
        model = DetallePedido
        fields = ['producto_id', 'cantidad']

        # Labels personalizados para el input
        labels = {
            'producto_id': 'Producto',
            'cantidad': 'Cantidad',
        }

        # Mensaje de error para cantidad
        error_messages = {
            'cantidad': {
                'required': 'La cantidad no puede estar vacía',
                'invalid': 'Debes ingresar un número válido'
            }
        }

        # Inputs y clases css
        widgets = {
            'producto_id': forms.Select(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400'}),
            'cantidad': forms.NumberInput(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Para que el select no tenga ---
        self.fields['producto_id'].empty_label = None
        

    # Validamos la cantidad
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        producto = self.cleaned_data.get('producto_id')
        
        # Si no se ha ingresado
        if cantidad is None:
            raise forms.ValidationError('La cantidad no puede estar vacia')
        
        # Si es 0 o negativa
        if cantidad <= 0:   
            raise forms.ValidationError('La cantidad debe ser mayor a 0')
        
        # Si no se ha seleccionado producto
        if producto is None:
            raise forms.ValidationError('Debes seleccionar un producto')

        # Si el stock del producto es 0 
        if producto.stock == 0: 
            raise forms.ValidationError('No hay stock disponible')

        # Si la cantidad superar el stock del producto
        if cantidad > producto.stock:
            raise forms.ValidationError(
                f"Solo hay {producto.stock} unidades disponibles")

        return cantidad

# Formset (varios formularios) para varios productos en el pedido
class BaseDetallePedidoFormSet(forms.BaseModelFormSet):
    def clean(self):
        # Si hay errores en los formularios individuales no hacemos validación adicional
        if any(self.errors):
            return

        # Array para almacenar los productos
        productos = []
        tiene_productos = False

        for form in self.forms:
            # Si el formulario está vacío (no se ha agregado un producto) lo ignoramos
            if not form.cleaned_data:
                continue

            producto = form.cleaned_data.get('producto_id')
            cantidad = form.cleaned_data.get('cantidad')
            
            # Si se ha ingresado producto y cantidad
            if producto and cantidad:
                tiene_productos = True

            # Si hay un producto ya ingresado
            if producto in productos:
                raise forms.ValidationError("No puedes repetir el mismo producto")

            # Agregamos al producto
            productos.append(producto)
            
        # Si no se ha ingresado ningún producto
        if not tiene_productos:
            raise forms.ValidationError("Debes agregar al menos un producto")

# Agregamos las reglas a formset
DetalleFormSet = forms.modelformset_factory(DetallePedido, form=DetallePedidoForm, formset=BaseDetallePedidoFormSet, extra=1)
