from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from datetime import date
from django.db.models.expressions import F
from django.core.validators import MaxValueValidator, MinValueValidator
from mapbox_location_field.models import LocationField
from django.utils.html import format_html
from django.core.validators import FileExtensionValidator

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
	ROLES = [
		('Employer', 'un employé'),
		('Associate', 'un associé'),
		('Employee', 'un employeur'),
	]
	email = models.EmailField(unique = True)
	profession = models.CharField(max_length = 100)
	formation = models.CharField(max_length = 100, null = True, blank = True)
	location = models.CharField(max_length = 100)
	diplome = models.CharField(max_length = 100, null = True, blank = True)
	contrat = models.CharField(max_length = 50, null = True, blank = True)
	is_staff = models.BooleanField(default = False)
	profile_pic = models.ImageField(null = True, blank = True, upload_to = 'profile_pics/')
	curriculum_vitae = models.FileField(null = True, blank = True,upload_to = 'curriculums/', validators = [FileExtensionValidator(allowed_extensions = ['pdf'])])
	date_joined = models.DateTimeField(default = timezone.now)
	is_active = models.BooleanField(default = True)
	first_name = models.CharField(max_length = 40)
	birthdate = models.DateField()
	last_name = models.CharField(max_length = 40)
	role = models.CharField(choices = ROLES, max_length = 10, default = "Employee")
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	
	objects = CustomUserManager()

	def __str__(self):
		return self.email

	def age(self):
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
		return format_html('<img src = "{}" width = "100" style = "border-radius : 50px" />'.format(self.profile_pic.url))

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