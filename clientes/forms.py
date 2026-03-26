
from django import forms

from clientes.models import Clientes


class ClientesForm(forms.ModelForm):
    class Meta:
        # Especificamos el modelo y los campos a incluir en el formulario
        model = Clientes
        fields = ['nombre', 'correo', 'direccion', 'telefono']

        # Mensajes de errores
        error_messages = {
            'nombre': {
                'required': 'El nombre no puede estar vacio'
            },
            'correo': {
                'required': 'El correo no puede estar vacio',
                'invalid': 'El correo no es valido'
            },
            'direccion': {
                'required': 'La direccion no puede estar vacia'
            },
            'telefono': {
                'required': 'El telefono no puede estar vacio'
            },
        }

        # Inputs y clases CSS de tailwind
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400'}),
            'correo': forms.EmailInput(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400'}),
            'direccion': forms.TextInput(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400'}),
            'telefono': forms.NumberInput(attrs={'class': 'block w-full bg-white focus:outline-none focus:shadow-outline border border-gray-300 rounded-md py-3 px-3  appearance-none leading-normal focus:border-blue-400'})
        }

    # Para validar el teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        # Si no se ha ingresado
        if telefono is None:
            raise forms.ValidationError('El telefono no puede estar vacio')
        
        
        if len(str(telefono)) < 10:
            raise forms.ValidationError('El telefono debe tener al menos 10 digitos')


        # Si no son dígitos
        if not telefono.isdigit():
            raise forms.ValidationError(
                'El telefono debe contener solo numeros')

        return telefono
