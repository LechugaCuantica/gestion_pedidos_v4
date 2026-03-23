from django.urls import path
from clientes import views


urlpatterns = [
    path('', views.listar_clientes, name='listar_clientes'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('ver/<int:cliente_id>/', views.ver_cliente, name='ver_cliente'),
    path('actualizar/<int:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('reporte_excel', views.reporte_clientes, name='reporte_clientes')
]
