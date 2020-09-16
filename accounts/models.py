from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from datetime import datetime
from django.db.models.expressions import F
from django.core.validators import MaxValueValidator, MinValueValidator
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(unique = True)
	is_staff = models.BooleanField(default = False)
	date_joined = models.DateTimeField(default = timezone.now)
	is_active = models.BooleanField(default = True)
	first_name = models.CharField(max_length = 40)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = CustomUserManager()

	def __str__(self):
		return self.email