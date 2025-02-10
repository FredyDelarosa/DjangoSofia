from django.shortcuts import render, redirect
from django.contrib.auth import login
from ..forms.register_form import CustomUserCreationForm

def register(request):
    print(f"Método de solicitud: {request.method}")  # Verifica si llega un POST

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        print(f"Datos recibidos: {request.POST}")  # Muestra los datos enviados

        if form.is_valid():
            user = form.save()
            print(f"Usuario creado: {user}")  # Confirma que el usuario se guardó
            login(request, user)  # Autentica al usuario
            return redirect('home')  # Redirigir al inicio

        print(f"Errores del formulario: {form.errors}")  # Muestra errores si hay
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})
