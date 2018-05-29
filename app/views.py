from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, models
from .forms import Login_Form, Id_Paciente_Form, Paciente_Form, Entrega_Form
from .models import Paciente, Entrega
from django.forms import formset_factory

# Create your views here.
def sign_in(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect("/")
	login_form = Login_Form(request.POST or None)
	msg = ''
	if login_form.is_valid():
		form_data = login_form.cleaned_data
		username = form_data.get('username')
		password = form_data.get('password')
		try:
			user = models.User.objects.get(username=username)
		except models.User.DoesNotExist:
			user = None
		if user is not None:
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect("/")
			else:
				msg = 'Contraseña incorrecta'
		else: 
			msg = 'No existe Usuario'

	context = {
		'login_form' : login_form,
		'msg' : msg,
	}
	return render(request, 'login.html', context)

def sign_out(request):
	logout(request)
	return HttpResponseRedirect("/")

def index(request):
	if request.user.is_authenticated:
		id_paciente_form = Id_Paciente_Form(request.POST or None)
		flag_exists = False
		flag_no_exists = False
		msg = ''
		paciente = None
		id = 0000000	
		if id_paciente_form.is_valid():
			form_data = id_paciente_form.cleaned_data
			id = form_data.get('id')
			try:
				paciente = Paciente.objects.get(id=id)
			except Paciente.DoesNotExist:
				paciente = None

			if paciente is not None:
				flag_exists = True
			else:
				msg = 'Paciente con id {} no existe'.format(id)
				flag_no_exists = True

		context = {
			'id_paciente_form' : id_paciente_form,
			'flag_exists' : flag_exists,
			'flag_no_exists' : flag_no_exists,
			'msg' : msg,
			'paciente' : paciente,
			'id' : id
		}
		return render(request, 'index.html', context)
	else:
		return HttpResponseRedirect("sign_in")

def agregar_paciente(request, id_paciente):
	if request.user.is_authenticated:
		paciente_form = Paciente_Form(request.POST or None)

		if paciente_form.is_valid():
			form_data = paciente_form.cleaned_data
			id = form_data.get('id')
			nombres = form_data.get('nombres')
			apellidos = form_data.get('apellidos')
			paciente = Paciente.objects.create(id=id, nombres=nombres, apellidos=apellidos)
			url = "/agregar_entrega/{}".format(id_paciente)
			return HttpResponseRedirect(url)

		context = {
			'paciente_form' : paciente_form,
			'id_paciente' : int(id_paciente)
		}
		return render(request, 'agregar_paciente.html', context)
	else:
		return HttpResponseRedirect("sign_in")

def agregar_entrega(request, id_paciente):
	if request.user.is_authenticated:
		entrega_form = Entrega_Form(request.POST or None)
		msg = ''
		if entrega_form.is_valid():
			form_data = entrega_form.cleaned_data
			id = form_data.get('id')
			paciente = form_data.get('paciente')
			despacho = request.user
			descripcion = form_data.get('descripcion')
			print(descripcion)
			entrega = Entrega.objects.create(id=id, despacho=despacho, descripcion=descripcion)
			entrega.paciente.add(paciente[0])
			msg = 'Entrega registrada correctamente'
			print(entrega.fecha)
			
		context = {
			'entrega_form' : entrega_form,
			'id_paciente' : int(id_paciente),
			'msg' : msg,
		}
		return render(request, 'agregar_entrega.html', context)
	else:
		return HttpResponseRedirect("sign_in")

def listar_entregas(request):
	if request.user.is_authenticated:
		paciente_form = Paciente_Form(request.POST or None)
		msg = ''
		mode = False
		entregas = Entrega.objects.all()

		print(entregas)
		if not len(entregas):
			msg = "No hay Mesas para listar"
		else:
			mode = True
		
		context = {
			'msg' : msg,
			'mode' : mode,
			'entregas' : entregas
		}
		return render(request, 'listar_entregas.html', context)
	else:
		return HttpResponseRedirect("sign_in")

def listar_entregas_user(request, id_paciente):
	if request.user.is_authenticated:
		paciente_form = Paciente_Form(request.POST or None)
		msg = ''
		mode = False
		entregas = Entrega.objects.all().filter(paciente=id_paciente)

		print(entregas)
		if not len(entregas):
			msg = "No hay Mesas para listar"
		else:
			mode = True
		
		context = {
			'msg' : msg,
			'mode' : mode,
			'entregas' : entregas,
			'id_paciente' : id_paciente
		}
		return render(request, 'listar_entregas.html', context)
	else:
		return HttpResponseRedirect("sign_in")