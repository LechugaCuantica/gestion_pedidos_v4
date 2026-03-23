from io import BytesIO

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
import xlsxwriter

from productos.forms import ProductosForm
from productos.models import Productos

# Create your views here.


def listar_productos(request: HttpRequest):
    # Obtenemos todos los productos desde la BD
    productos = Productos.objects.all()

    # Paginación de 5
    paginator = Paginator(productos, 5)

    # Página actual desde los parámetros de URL
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Renderizamos template con paginador
    return render(request, 'productos/listar_productos.html', {'page_obj': page_obj})


def ver_producto(request: HttpRequest, id: int):
    # Obtenemos producto por ID
    producto = Productos.objects.get(id=id)

    # Renderizamos detalles del producto
    return render(request, 'productos/ver_producto.html', {'producto': producto})


def crear_producto(request: HttpRequest):
    # Si es POST validamos y guardamos
    if request.method == 'POST':
        form = ProductosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductosForm()

    # Renderizamos formulario de creación
    return render(request, 'productos/crear_producto.html', {'form': form})


def actualizar_producto(request: HttpRequest, id: int):
    # Obtenemos producto existente
    producto = Productos.objects.get(id=id)

    if request.method == 'POST':
        form = ProductosForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductosForm(instance=producto)

    # Renderizamos formulario con datos actuales
    return render(request, 'productos/actualizar_producto.html', {'form': form, 'producto': producto})


def eliminar_producto(request: HttpRequest, id: int):
    # Obtenemos y eliminamos producto
    producto = Productos.objects.get(id=id)
    producto.delete()

    # Retornamos JSON de confirmación
    return JsonResponse({'msg': 'Producto eliminado correctamente'})


def reporte_productos(request: HttpRequest):
    # Obtenemos todos los productos
    productos = Productos.objects.all()

    # Trabajamos el archivo en memoria
    buffer = BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    sheet = workbook.add_worksheet()

    # Encabezados de la hoja
    sheet.write(0, 0, 'ID')
    sheet.write(0, 1, 'Producto')
    sheet.write(0, 2, 'Precio')
    sheet.write(0, 3, 'Stock')

    # Llenamos datos
    row = 1
    # Recorremos todos los productos
    for producto in productos:
        sheet.write(row, 0, producto.id)
        sheet.write(row, 1, producto.nombre)
        sheet.write(row, 2, producto.precio)
        sheet.write(row, 3, producto.stock)
        row += 1

    # Cerramos el workbook y regresamos desde el inicio del buffer
    workbook.close()
    buffer.seek(0)

    return HttpResponse(buffer, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={'Content-Disposition': 'attachment; filename="reporte_productos.xlsx"'})
