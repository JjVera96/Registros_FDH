from django import forms
from .models import Paciente, Entrega

class Login_Form(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50)

class Id_Paciente_Form(forms.Form):
	id = forms.CharField(max_length=50)

class Paciente_Form(forms.ModelForm):	
	class Meta:
		model = Paciente
		fields = ['id', 'nombres', 'apellidos']

class Entrega_Form(forms.ModelForm):
	class Meta:
		model = Entrega
		fields = ['paciente', 'id', 'descripcion']
