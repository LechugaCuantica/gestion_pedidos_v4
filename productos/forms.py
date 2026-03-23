
from django import forms

from productos.models import Productos


class ProductosForm(forms.ModelForm):
    class Meta:
        # Especificamos el modelo y los campos a incluir en el formulario
        model = Productos
        fields = ['nombre', 'precio', 'stock']
        
        # Mensajes de error
        error_messages ={
            'nombre': {
                'required': 'El nombre no puede estar vacio'
            },
            'precio': {
                'required': 'El precio no puede estar vacio'
            },
            'stock': {
                'required': 'El stock no puede estar vacio'
            }
        }
         # Inputs y sus clases css
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400'}),
            'precio': forms.NumberInput(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400'}),
            'stock': forms.NumberInput(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400'})
        }

    # Validamos el precio
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        
        # Si no se ha ingresado
        if precio is None:
            raise forms.ValidationError('El precio no puede estar vacio')
        
        # Si es menor a 0
        if precio <= 0:
            raise forms.ValidationError('El precio no puede ser menor o igual a 0')
        
        return precio
    
    # Validamos el stock
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        
        # Si no se ha ingresado el stock
        if stock is None:
            raise forms.ValidationError('El stock no puede estar vacio')
        
        # si el stock es negativo
        if stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo')
        
        return stock
        
    