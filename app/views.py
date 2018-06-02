from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, models
from .forms import Login_Form, Id_Paciente_Form, Paciente_Form, Entrega_Form, Buscar_Form, Change_Form, User_Form, Edit_User_Form
from django.contrib.auth.hashers import make_password
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
			entrega = Entrega.objects.create(id=id, despacho=despacho, descripcion=descripcion)
			entrega.paciente.add(paciente[0])
			msg = 'Entrega registrada correctamente'
			
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
		msg = ''
		mode = False
		entregas = Entrega.objects.all()

		if not len(entregas):
			msg = "No hay Entregas para mostrar"
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
		msg = ''
		mode = False
		entregas = Entrega.objects.all().filter(paciente=id_paciente)
		if not len(entregas):
			msg = "No hay Entregas para mostrar"
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

def buscar_entrega(request):
	if request.user.is_authenticated:
		buscar_form = Buscar_Form(request.POST or None)
		entregas = []
		mode = False
		msg = ''
		id_paciente = None

		if buscar_form.is_valid():
			form_data = buscar_form.cleaned_data
			id_paciente = form_data.get('id_paciente')
			id_entrega = form_data.get('id_entrega')

			if id_paciente and id_entrega:
				entregas = Entrega.objects.all().filter(paciente=id_paciente, id=id_entrega)
			elif id_paciente:
				entregas = Entrega.objects.all().filter(paciente=id_paciente)
			elif id_entrega:
				entregas = Entrega.objects.all().filter(id=id_entrega)

			if not len(entregas):
				msg = "No hay Entregas para mostrar"
			else:
				mode = True

		context = {
			'buscar_form' : buscar_form,
			'entregas': entregas,
			'msg' : msg,
			'mode' : mode,
			'id_paciente' : id_paciente
		}
		return render(request, 'buscar_entrega.html', context)
	else:
		return HttpResponseRedirect("sign_in")

def cuenta(request):
	if request.user.is_authenticated:
		context = {
		}
		return render(request, 'cuenta.html', context)
	else:
		return HttpResponseRedirect("sign_in")

def cambiar_contrasena(request, id_user):
	if request.user.is_authenticated:
		if request.user.id == id_user or request.user.is_staff:
			user = models.User.objects.get(id=id_user)
			change_form = Change_Form(request.POST or None)
			msg = ''
			
			if change_form.is_valid():
				form_data = change_form.cleaned_data
				password = form_data.get('password')
				again = form_data.get('again')
				if password == again:
					user.password = make_password(password, salt=None, hasher='default')
					user.save()
					msg = "Contraseña Cambiada correctamente"
				else:
					msg = "Contraseña no Coinciden"
			context = {
				'change_form': change_form,
				'msg' : msg,
				'p_user' : user

			}
			return render(request, 'cambiar_contrasena.html', context)
		else:
			return HttpResponseRedirect("sign_in")
	else:
		return HttpResponseRedirect("sign_in")

def empleados(request):
	if request.user.is_authenticated and request.user.is_staff:
		msg = ''
		mode = False
		empleados = models.User.objects.all()
		if not len(empleados):
			msg = "No hay empleados para mostrar"
		else:
			mode = True
		
		context = {
			'msg' : msg,
			'mode' : mode,
			'empleados' : empleados
		}
		return render(request, 'empleados.html', context)
	else:
		return HttpResponseRedirect("sign_in")

def crear_empleado(request):
	if request.user.is_authenticated and request.user.is_staff:

		user_form = User_Form(request.POST or None)
		msg = ''
		if user_form.is_valid():
			form_data = user_form.cleaned_data
			username = form_data.get('username')
			first_name = form_data.get('first_name')
			last_name = form_data.get('last_name')
			password = form_data.get('password')
			user = models.User.objects.create_user(username, first_name=first_name, last_name=last_name, password=password)
			msg = 'Empleado registrado correctamente'
			
		context = {
			'user_form' : user_form,
			'msg' : msg,
		}

		return render(request, 'crear_empleado.html', context)
	else:
		return HttpResponseRedirect("sign_in")

def editar_empleado(request, id_user):
	if request.user.is_authenticated and request.user.is_staff:
	
		e_user = models.User.objects.get(id=id_user)
		edit_user_form = Edit_User_Form(request.POST or None, instance=e_user)
		if edit_user_form.is_valid():
			form_data = edit_user_form.cleaned_data
			e_user.username = form_data.get('username')
			e_user.first_name = form_data.get('first_name')
			e_user.last_name = form_data.get('last_name')
			e_user.active = form_data.get('is_active')
			e_user.save()
			url = '/editar_empleado/{}'.format(id_user)
			return HttpResponseRedirect(url)

		context = {
			'e_user' : e_user
		}

		return render(request, 'editar_empleado.html', context)
	else:
		return HttpResponseRedirect("sign_in")