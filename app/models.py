from django.db import models

# Create your models here.
class Paciente(models.Model):
	id = models.CharField(max_length=20, primary_key=True)
	nombres = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=50)
	
	def __str__(self):
		return str(self.id)

class Entrega(models.Model):
	id = models.CharField(max_length=20, primary_key=True)
	paciente = models.ManyToManyField('Paciente')
	fecha = models.DateTimeField(auto_now_add=True, auto_now=False)
	despacho = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=300)

	def __str__(self):
		return str(self.id)

class Medicamento(models.Model):
	id = models.AutoField(primary_key=True)
	entrega = models.ForeignKey(Entrega, on_delete=models.DO_NOTHING)
	nombre = models.CharField(max_length=50)
	cantidad = models.IntegerField()

	def __str__(self):
		return str(self.id)
