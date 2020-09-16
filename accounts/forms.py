from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from datetime import datetime
from django.forms.widgets import PasswordInput, TextInput, NumberInput, DateInput, EmailInput, Select
from django.forms import ModelForm
from .models import CustomUser
from encountr import settings

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'first_name')


class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ('email', 'first_name')