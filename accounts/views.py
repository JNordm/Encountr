from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import HttpResponse

from .forms import CustomUserCreationForm, CustomUserChangeForm, UploadFileForm, CustomUserStatusForm
from .models import CustomUser, Profession, Formation, Location, Diplome
from .resources import ProfessionResource
# Create your views here.

@login_required
def profilePage(request):
	user = request.user
	return render (request, 'accounts/profile.html', locals())

def editProfile(request):
	if request.method == 'POST':
		form = CustomUserChangeForm(request.POST, request.FILES, instance = request.user)
		if form.is_valid(): 
			form.save()
			messages.success(request, 'Votre compte a bien été mis à jour !')
			return redirect('profilePage')
		else : 
			return render(request, 'accounts/edit.html',locals())
	else:
		form = CustomUserChangeForm(instance = request.user)
		return render(request, 'accounts/edit.html', locals())

def editRole(request):
	if request.method == "POST":
		form = CustomUserStatusForm(request.POST, instance = request.user)
		if form.is_valid:
			form.save()
			messages.success(request, 'Votre compte a bien été mis à jour !')
			return redirect('profilePage')
		else : 
			return render(request, 'accounts/editrole.html', locals())
	else:
		form = CustomUserStatusForm(instance = request.user)
		return render(request, 'accounts/editrole.html', locals())

def editPassword(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data = request.POST, user = request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Votre nouveau mot de passe a bien été enregistré !')
			update_session_auth_hash(request, form.user)
			return redirect('profilePage')
		else:
			return redirect('editPassword')
	else:
		form = PasswordChangeForm(user = request.user)
	
	return render(request, 'accounts/editpassword.html', locals())	


def activateUser(request, uidb64, token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = CustomUser._default_manager.get(pk=uid)
	except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
		user = None
	if user is not None and default_token_generator.check_token(user, token):
		user.is_active=True
		user.save()
		first_name = user.first_name
		messages.success(request, 'Bienvenue sur Encountr,' + ' ' + first_name + ' !') 
		messages.success(request, 'Votre compte a été activé, veuillez maintenant vous connecter pour accéder à votre compte.')
		return redirect('homePage')
	else : 
		return HttpResponse("Votre lien d'activation est invalide !")

def logoutUser(request):
	logout(request)
	return redirect('homePage')


from tablib import Dataset

def simple_upload_formation(request):
	if request.method == 'POST':
		formation_resource = FormationResource()
		dataset = Dataset()
		new_formation = request.FILES['myfile']

		imported_data = dataset.load(new_formation.read())
		result = formation_resource.import_data(dataset, dry_run=True)  # Test the data import

		if not result.has_errors():
			formation_resource.import_data(dataset, dry_run=False)  # Actually import now

	return redirect('homePage')

def simple_upload_profession(request):
	if request.method == 'POST':
		profession_resource = professionResource()
		dataset = Dataset()
		new_profession = request.FILES['myfile']

		imported_data = dataset.load(new_profession.read())
		result = profession_resource.import_data(dataset, dry_run=True)  # Test the data import

		if not result.has_errors():
			profession_resource.import_data(dataset, dry_run=False)  # Actually import now

	return redirect('homePage')

def simple_upload_location(request):
	if request.method == 'POST':
		location_resource = locationResource()
		dataset = Dataset()
		new_location = request.FILES['myfile']

		imported_data = dataset.load(new_location.read())
		result = location_resource.import_data(dataset, dry_run=True)  # Test the data import

		if not result.has_errors():
			location_resource.import_data(dataset, dry_run=False)  # Actually import now

	return redirect('homePage')

def simple_upload_diplome(request):
	if request.method == 'POST':
		diplome_resource = diplomeResource()
		dataset = Dataset()
		new_diplome = request.FILES['myfile']

		imported_data = dataset.load(new_diplome.read())
		result = diplome_resource.import_data(dataset, dry_run=True)  # Test the data import

		if not result.has_errors():
			diplome_resource.import_data(dataset, dry_run=False)  # Actually import now

	return redirect('homePage')