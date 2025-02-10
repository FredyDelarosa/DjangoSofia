from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150, 
        label="Usuario", 
        widget=forms.TextInput(attrs={'placeholder': 'Ej: sofia'})
    )
    password1 = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Ej: 12345678a'})
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Repetir contraseña'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_password2(self):
        """Evita las validaciones de seguridad de Django."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return password2  # Permite cualquier contraseña
