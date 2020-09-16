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

from .forms import CustomUserCreationForm
from .models import CustomUser

# Create your views here.

@login_required
def profilePage(request):
	email = request.user.email
	first_name = request.user.first_name
	return render (request, 'accounts/profile.html', locals())

def editProfile(request):
	if request.method == 'POST':
		form = CustomUserChangeForm(request.POST, instance = request.user)
		if form.is_valid : 
			form.save()
			messages.success(request, 'Votre compte a bien été mis à jour !')
			return redirect('profilePage')
	else:
		form = CustomUserChangeForm(instance = request.user)
		return render(request, 'accounts/edit.html', locals())

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

def registerPage(request):
	form = CustomUserCreationForm()
	if request.method == 'POST':
			form = CustomUserCreationForm(request.POST)
			if form.is_valid():
				first_name = form.cleaned_data.get('first_name')
				user = form.save()
				user.is_active = False
				user.save()
				current_site = get_current_site(request)
				subject= 'Activate your account - Thanks for signing up at Encountr !'
				message = render_to_string('accounts/email.html',
					{
						'user':user,
						'domain':current_site.domain,
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'token': default_token_generator.make_token(user),
					})
				from_email = settings.EMAIL_HOST_USER
				mail_to = [form.cleaned_data.get('email'), settings.EMAIL_HOST_USER]
				send_mail(subject, message, from_email, mail_to, fail_silently = False)
			return redirect('activatePage')
	return render (request, 'accounts/register.html', locals())


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
		return redirect('loginPage')
	else : 
		return HttpResponse("Votre lien d'activation est invalide !")

def loginPage(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request, email = email, password = password)
		if user is not None:
			login(request, user)
			return redirect('profilePage')
		else:
			messages.info(request, "Le mot de passe ou l'adresse mail fourni(e) est incorrect(e) ! Essayez à nouveau...")
	
	return render (request, 'accounts/login.html', locals())

def logoutUser(request):
	logout(request)
	return redirect('loginPage')