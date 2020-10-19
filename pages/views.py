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
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser

# Create your views here.

def homePage(request):
	form = CustomUserCreationForm()
	if request.method == 'POST':
			form = CustomUserCreationForm(request.POST)
			if form.is_valid():
				first_name = form.cleaned_data.get('first_name')
				user = form.save()
				user.is_active = False
				user.save()
				password = form.cleaned_data.get('password1')
				try :
					validate_password(password, user)
				except ValidationError as e : 
					form.add_error('password', e)
					return render(request, 'page/home.html', locals())
				current_site = get_current_site(request)
				subject= 'Activez votre compte - Encountr'
				message = render_to_string('pages/email.html',
					{
						'user':user,
						'domain':current_site.domain,
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'token': default_token_generator.make_token(user),
					})
				plain_message = strip_tags(message)
				from_email = settings.EMAIL_HOST_USER
				mail_to = [form.cleaned_data.get('email'), settings.EMAIL_HOST_USER]
				send_mail(subject, plain_message, from_email, mail_to, fail_silently = False)
				return redirect('activatePage')
	return render(request, 'pages/home.html', locals())

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
	return redirect('homePage')