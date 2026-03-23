from io import BytesIO

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import xlsxwriter

from clientes.forms import ClientesForm
from clientes.models import Clientes
from django.core.paginator import Paginator

# Create your views here.


def listar_clientes(request: HttpRequest):
    # Obtenemos todos los clientes
    clientes = Clientes.objects.all()

    # Paginación de 5
    paginator = Paginator(clientes, 5)

    # Página actual
    page_number = request.GET.get('page')

    # Objeto de la paginación
    page_obj = paginator.get_page(page_number)

    # renderizamos la vista
    return render(request, 'clientes/listar_clientes.html', {'page_obj': page_obj})


def crear_cliente(request: HttpRequest):
    # Si el metodo es POST
    if request.method == 'POST':
        form = ClientesForm(request.POST)
        # Validamos el formulario
        if form.is_valid():
            # Guardamos y redirecciionamos al listado de clientes
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClientesForm()
    # De lo contrario renderizamos la vista
    return render(request, 'clientes/crear_cliente.html', {'form': form})


def ver_cliente(request: HttpRequest, cliente_id: int):
    # Obtenemos el cliente especifico
    cliente = Clientes.objects.get(pk=cliente_id)
    # Renderizamos la vista con la info
    return render(request, 'clientes/ver_cliente.html', {'cliente': cliente})


def actualizar_cliente(request: HttpRequest, cliente_id: int):
    cliente = get_object_or_404(Clientes, pk=cliente_id)

    # Si el metodo es POST
    if request.method == 'POST':
        form = ClientesForm(request.POST, instance=cliente)
        # Válidamos el formulario
        if form.is_valid():
            # Guardamos y redireccionamos al listado de clientes
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClientesForm(instance=cliente)

    # Renderizamos la vista del formulario
    return render(request, 'clientes/actualizar_cliente.html', {'form': form, 'cliente': cliente})


def eliminar_cliente(request: HttpRequest, cliente_id: int):
    # Obtenemos el cliente especifico
    cliente = get_object_or_404(Clientes, pk=cliente_id)
    # Lo eliminamos
    cliente.delete()

    # Respondemos en formato JSON para el mensaje de la alerta
    return JsonResponse({'msg': 'Cliente eliminado correctamente'})


def reporte_clientes(request: HttpResponse):
    # Obtenemos todos los clientes
    clientes = Clientes.objects.all()

    # para no guardar el archivo
    buffer = BytesIO()

    # Creamos el libro
    workbook = xlsxwriter.Workbook(buffer)
    # Añadimos una hoja
    sheet = workbook.add_worksheet()

    # Ponemos los encabezados
    sheet.write(0, 0, "ID")
    sheet.write(0, 1, "Nombre")
    sheet.write(0, 2, "Correo")
    sheet.write(0, 3, "Dirección")
    sheet.write(0, 4, "Teléfono")

    row = 1
    # Recorremos todos los clientes
    for cliente in clientes:
        sheet.write(row, 0, cliente.id)
        sheet.write(row, 1, cliente.nombre)
        sheet.write(row, 2, cliente.correo)
        sheet.write(row, 3, cliente.direccion)
        sheet.write(row, 4, cliente.telefono)
        row += 1

    # Cerramos
    workbook.close()

    # Volvemos al inicio del buffer para leer bien el archivo al enviarlo
    buffer.seek(0)

    return HttpResponse(buffer, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={'Content-Disposition': 'attachment; filename="reporte_clientes.xlsx"'})
