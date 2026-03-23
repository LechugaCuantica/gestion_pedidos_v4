from io import BytesIO

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from pedidos.forms import DetalleFormSet, PedidosForm
from pedidos.models import DetallePedido, Pedidos
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# Create your views here.

def listar_pedidos(request: HttpRequest):
    # Obtenemos todos los pedidos
    pedidos = Pedidos.objects.all()

    # Paginación de 10
    paginator = Paginator(pedidos, 10)

    # Página actual desde query params
    page_number = request.GET.get('page')

    # Objeto de paginación con la página
    page_obj = paginator.get_page(page_number)

    # Renderizamos la lista de pedidos
    return render(request, 'pedidos/listar_pedidos.html', {'page_obj': page_obj})


def crear_pedido(request: HttpRequest):
    # Si el método es POST procesamos el formulario
    if request.method == 'POST':
        form = PedidosForm(request.POST)
        formset = DetalleFormSet(
            request.POST, queryset=DetallePedido.objects.none())

        # Si el pedido y sus detalles son válidos, guardamos todo
        if form.is_valid() and formset.is_valid():
            pedido = form.save()
            detalles = formset.save(commit=False)

            for detalle in detalles:
                # Asociamos detalle al pedido y calculamos subtotal
                detalle.pedido_id = pedido
                detalle.subtotal = detalle.producto_id.precio * detalle.cantidad

                # Restamos stock del producto en base a la cantidad vendida
                producto = detalle.producto_id
                producto.stock -= detalle.cantidad
                producto.save()

                detalle.save()

            return redirect('listar_pedidos')
    else:
        form = PedidosForm()
        formset = DetalleFormSet(queryset=DetallePedido.objects.none())

    # Renderizamos formulario vacío para crear pedido
    return render(request, 'pedidos/crear_pedido.html', {'form': form, 'formset': formset})


def ver_pedido(request: HttpRequest, pedido_id: int):
    # Obtenemos el pedido y sus detalles
    pedido = Pedidos.objects.get(id=pedido_id)
    detalles = DetallePedido.objects.filter(pedido_id=pedido_id)

    # Renderizamos la vista de detalles del pedido
    return render(request, 'pedidos/ver_pedido.html', {'pedido': pedido, 'detalles': detalles})


def actualizar_pedido(request: HttpRequest, pedido_id: int):
    # Obtenemos el pedido a actualizar
    pedido = Pedidos.objects.get(id=pedido_id)

    if request.method == 'POST':
        form = PedidosForm(request.POST, instance=pedido)

        # Guardamos cambios si es válido
        if form.is_valid():
            form.save()
            return redirect('listar_pedidos')
    else:
        form = PedidosForm(instance=pedido)

    # Renderizamos formulario con datos existentes
    return render(request, 'pedidos/actualizar_pedido.html', {'form': form})


def eliminar_pedido(request: HttpRequest, pedido_id: int):
    # Obtenemos pedido y sus detalles relacionados
    pedido = Pedidos.objects.get(id=pedido_id)
    detallePedido = DetallePedido.objects.filter(pedido_id=pedido_id)

    # No permitir eliminar si tiene detalles
    if len(detallePedido) > 0:
        return JsonResponse({'msg': 'El pedido tiene detalles, no se puede eliminar debido a esto.'}, status=400)

    pedido.delete()
    return JsonResponse({'msg': 'Pedido eliminado correctamente'})


def reporte_pdf(request: HttpRequest, id_pedido: int):
    # Obtenemos el pedido y sus detalles para generar PDF
    pedido = Pedidos.objects.get(id=id_pedido)
    detalles = DetallePedido.objects.filter(pedido_id=id_pedido)

    buffer = BytesIO()

    # Inicializamos canvas PDF
    cc = canvas.Canvas(buffer, pagesize=letter)

    cc.setFont('Helvetica-Bold', 22)
    cc.drawString(100, 750, 'REPORTE DEL PEDIDO')

    cc.setFont('Helvetica', 16)
    cc.drawString(100, 700, f'ID: {pedido.id}')
    cc.drawString(100, 670, f'Cliente: {pedido.cliente}')
    cc.drawString(100, 640, f'Fecha: {pedido.fecha}')
    cc.drawString(100, 610, f'Estado: {pedido.estado}')

    cc.setFont('Helvetica-Bold', 22)
    cc.drawString(100, 550, 'Detalles del pedido:')
    cc.setFont('Helvetica', 16)

    y = 500
    total = 0
    # Recorremos todos los detalles del pedido y lo escribimos
    for detalle in detalles:
        cc.drawString(100, y, f'Producto: {detalle.producto_id}')
        y -= 20
        cc.drawString(100, y, f'Cantidad: {detalle.cantidad}')
        y -= 20
        cc.drawString(100, y, f'Subtotal: {detalle.subtotal:,.2f}')
        y -= 40
        total += detalle.subtotal

    cc.setFont('Helvetica-Bold', 22)
    cc.drawString(100, y, f'Total del pedido: {total:,.2f}')

    cc.showPage()
    cc.save()

    # Devolver PDF generado
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf', headers={'Content-Disposition': f'attachment; filename="reporte_pedido_{pedido.id}_{pedido.cliente}.pdf"'})
