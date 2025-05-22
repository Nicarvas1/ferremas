from django.contrib.auth.forms import UserCreationForm
from .models import Usuario  # tu modelo personalizado

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "email")  # agrega los campos que uses