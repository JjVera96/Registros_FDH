from django import forms
from .models import Paciente, Entrega
from django.contrib.auth.models import User

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

class Buscar_Form(forms.Form):
	id_paciente = forms.CharField(max_length=50, required=False)
	id_entrega = forms.CharField(max_length=50, required=False)

class Change_Form(forms.Form):
	password = forms.CharField(max_length=50)
	again = forms.CharField(max_length=50)

class User_Form(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'password']

class Edit_User_Form(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'is_active']