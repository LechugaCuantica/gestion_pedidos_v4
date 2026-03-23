from django.urls import path

from productos import views


urlpatterns = [
    path('', views.listar_productos, name='listar_productos'),
    path('ver/<int:id>', views.ver_producto, name='ver_producto'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('editar/<int:id>', views.actualizar_producto, name='actualizar_producto'),
    path('eliminar/<int:id>', views.eliminar_producto, name='eliminar_producto'),
    path('reporte_productos', views.reporte_productos, name='reporte_productos')
]
