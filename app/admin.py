from django.contrib import admin

# Register your models here.
from .models import Paciente, Entrega

admin.site.register(Paciente)
admin.site.register(Entrega)
