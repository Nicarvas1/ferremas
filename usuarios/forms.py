from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import Usuario

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'telefono', 'password1', 'password2', 'rol')
