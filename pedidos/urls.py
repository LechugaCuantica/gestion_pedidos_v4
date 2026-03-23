
from django.urls import path

from pedidos import views


urlpatterns = [
    path('', views.listar_pedidos, name='listar_pedidos'),
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path("ver/<int:pedido_id>/", views.ver_pedido, name="ver_pedido"),
    path('actualizar/<int:pedido_id>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('eliminar/<int:pedido_id>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('reporte/<int:id_pedido>/', views.reporte_pdf, name='reporte_pdf')
]
