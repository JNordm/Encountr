from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from datetime import date
from django.db.models.expressions import F
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.html import format_html
from django.core.validators import FileExtensionValidator

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
	#Modèle d'utilisateur de Encountr  comprenant les trois profils disponibles.
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

	#information générales
	role = models.CharField(choices = ROLES, max_length = 10, default = "Employee") 
	first_name = models.CharField(max_length = 40)
	last_name = models.CharField(max_length = 40)
	birthdate = models.DateField()
	email = models.EmailField(unique = True)
	profession = models.CharField(max_length = 100)
	location = models.CharField(max_length = 100)
	profile_pic = models.ImageField(null = True, blank = True, upload_to = 'profile_pics/')
	
	#employeur et employé
	contrat = models.CharField(max_length = 50, null = True, blank = True)

	#employé uniquement
	formation = models.CharField(max_length = 100, null = True, blank = True)
	diplome = models.CharField(max_length = 100, null = True, blank = True)
	curriculum_vitae = models.FileField(null = True, blank = True,upload_to = 'curriculums/', validators = [FileExtensionValidator(allowed_extensions = ['pdf'])])
	is_first_job = models.BooleanField(null = True, blank = True, default = False)
	last_company = models.CharField(null = True, blank = True, default = '', max_length = 100)

	
	#employeur uniquement

	#associé uniquement

	#informations techniques
	is_staff = models.BooleanField(default = False)
	is_active = models.BooleanField(default = True)
	date_joined = models.DateTimeField(default = timezone.now)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	
	objects = CustomUserManager()

	def __str__(self):
		return self.email


	def age(self):
	#retourne l'âge du nouvel inscrit
		today = date.today()
		try: 
			birthday = self.birthdate.replace(year=today.year)
		except ValueError: # raised when birth date is February 29 and the current year is not a leap year
			birthday = self.birhdate.replace(year=today.year, month=born.month+1, day=1)
		if birthday > today:
			return today.year - self.birthdate.year - 1
		else:
			return today.year - self.birthdate.year

	def profile_image(self):
	#permet d'afficher la photo de profil dans l'administration
		return format_html('<img src = "{}" width = "100" style = "border-radius : 50px" />'.format(self.profile_pic.url))

#modèles pour les datalist
class Profession(models.Model):
	name = models.CharField(max_length = 200)

	def __str__(self):
		return self.name

class Formation(models.Model) :
	name = models.CharField(max_length = 200)

	def __str__(self):
		return self.name

class Location(models.Model) :
	name = models.CharField(max_length = 200)

	def __str__(self):
		return self.name

class Diplome(models.Model) :
	name = models.CharField(max_length = 200)

	def __str__(self):
		return self.name