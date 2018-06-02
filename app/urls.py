from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('agregar_paciente/<int:id_paciente>', views.agregar_paciente, name='agregar_paciente'),
    path('agregar_entrega/<int:id_paciente>', views.agregar_entrega, name='agregar_entrega'),
    path('listar_entregas', views.listar_entregas, name='listar_entregas'),
    path('listar_entregas/<int:id_paciente>', views.listar_entregas_user, name='listar_entregas_user'),
    path('buscar_entrega', views.buscar_entrega, name='buscar_entrega'),
    path('cuenta', views.cuenta, name='cuenta'),
    path('cambiar_contrasena/<int:id_user>', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('empleados', views.empleados, name='empleados'),
    path('crear_empleado', views.crear_empleado, name='crear_empleado'),
    path('editar_empleado/<int:id_user>', views.editar_empleado, name='editar_empleado'),
]