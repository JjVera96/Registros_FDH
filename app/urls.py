from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('agregar_paciente/<int:id_paciente>', views.agregar_paciente, name='agregar_paciente'),
    path('agregar_entrega/<int:id_paciente>', views.agregar_entrega, name='agregar_entrega'),
]