from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from datetime import date
from django.forms.widgets import PasswordInput, TextInput, NumberInput, DateInput, EmailInput, Select
from django.forms import ModelForm
from django.core.validators import RegexValidator
from .models import CustomUser, Profession, Formation, Location, Diplome
from encountr import settings
from .fields import ListTextWidget

ROLES = [
		('Employer', 'un employé'),
		('Associate', 'un associé'),
		('Employee', 'un employeur'),
	]

CONTRATS = [
		('CDI', 'CDI - Contrat à durée indéterminée'), 
		('CDD', 'CDD - Contrat à durée déterminée'), 
		('CAA', "Contrat d'apprentissage - Alternance"), 
		('CPA', "Contrat de professionnalisation - Alternance"), 
		('CUI', "CUI - Contrat unique d'insertion"),
	]
BOOL_CHOICES = [
		(True, 'Oui'),
		(False, 'Non'),
	]

class CustomUserCreationForm(UserCreationForm):

	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('email', 'first_name', 'birthdate', 'role', 'last_name')
		widgets = {
			'email':forms.EmailInput(attrs = {'placeholder' : "Quel est votre email ?", "id" : "email"}),
			'first_name':forms.TextInput(attrs = {'placeholder' : "Votre prénom ?", "id" : "firstname"}),
			'birthdate': forms.DateInput(attrs = {'placeholder':"Votre date de naissance ?", "id":"datepicker", "class":"datepicker"}),
			'role':forms.Select(choices = ROLES, attrs = {'placeholder':"Vous recherchez", "id":"role-input", "class":"role-input"}),
			'last_name': forms.TextInput(attrs = {'placeholder': "Votre nom ?", "id":"lastname"}),
		}

	def __init__(self, *args, **kwargs):
		super(CustomUserCreationForm, self).__init__(*args, **kwargs)
		self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': "Choisissez-vous un mot de passe", "id" : "password1"})
		self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': "Confirmez votre mot de passe", "id" : "password2"})


	def clean_password2(self):
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']
		if password2 != password1 :
			raise forms.ValidationError('Les deux mots de passe ne correspondent pas.')
		return password2

	def clean_birthdate(self):
		birthdate = self.cleaned_data["birthdate"]
		today = date.today()
		try: 
			birthday = birthdate.replace(year=today.year)
		except ValueError: # raised when birth date is February 29 and the current year is not a leap year
			birthday = birthdate.replace(year=today.year, month=born.month+1, day=1)
		if birthday > today:
			birthdate_delta = today.year - birthdate.year - 1
		else:
			birthdate_delta = today.year - birthdate.year
		if birthdate_delta < 18:
			raise forms.ValidationError('Vous devez être majeur pour poursuivre.')
		return birthdate

class CustomUserStatusForm(UserChangeForm):

	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('role', )
		widgets = {
			'role':forms.Select(choices = ROLES, attrs = {'placeholder':"Vous recherchez", "id":"role-input", "class":"role-input"}),
		}

class CustomUserChangeForm(UserChangeForm):
	
	class Meta:
		results_profession = Profession.objects.all()
		results_formation = Formation.objects.all()
		results_location = Location.objects.all()
		results_diplome = Diplome.objects.all()
		model = CustomUser
		fields = 	('email', 'first_name', 'birthdate', 
					'last_name', 'role', 'profession', 
					'formation', 'location', 'profile_pic', 
					'curriculum_vitae', 'contrat', 'diplome', 
					'is_first_job', 'last_company',)
		widgets = {
			'email': EmailInput(attrs= {'class' : 'userinput'}),
			'first_name' : TextInput(attrs= {'class' : 'userinput'}),
			'last_name' : TextInput(attrs= {'class' : 'userinput'}),
			'birthdate' : DateInput(attrs= {'class' : 'userinput'}),
			'last_company' : TextInput(attrs= {'class' : 'userinput'}),
			'profession': ListTextWidget(data_list = results_profession, name = 'profession-list', attrs= {'class' : 'userinput'}),
			'formation': ListTextWidget(data_list = results_formation, name = 'formation-list', attrs= {'class' : 'userinput'}),
			'location': ListTextWidget(data_list = results_location, name = 'location-list', attrs= {'class' : 'userinput'}),
			'diplome': ListTextWidget(data_list = results_diplome, name = 'diplome-list', attrs= {'class' : 'userinput'}),
			'contrat': forms.Select(choices = CONTRATS ),
			'is_first_job' : forms.CheckboxInput(attrs = {'id' : 'is_first_job', 'class':'is_first_job', 'onclick':'hideForm(this)'})
		}

class UploadFileForm(forms.Form):
	file = forms.FileField()