from django.shortcuts import render, redirect
from transbank.webpay.webpay_plus.transaction import Transaction
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def index(request):
    return render(request, 'index.html')

def webpay_init_transaction(request):
    tx = Transaction(
        commerce_code='597020000540',  # Código de comercio de prueba
        api_key='022c0a599bfa4bc0a7a5e5c3a5e5c3a5',
        environment='TEST'  # ambiente de pruebas
    )
    buy_order = 'orden1234'
    session_id = 'usuario123'
    amount = 10000  # monto de prueba
    return_url = 'http://localhost:8000/api/webpay/return/'  # Donde volverá el usuario tras pagar

    response = tx.create(buy_order, session_id, amount, return_url)
    # Esto te devuelve una URL (redirect_url) donde debes redirigir al usuario para que pague en Webpay
    return JsonResponse({
        "url": response['url'],
        "token": response['token']
    })

def webpay_return(request):
    token = request.GET.get('token_ws')
    tx = Transaction(
        commerce_code='597020000540',
        api_key='022c0a599bfa4bc0a7a5e5c3a5e5c3a5',
        environment='TEST'
    )
    result = tx.commit(token)
    # Aquí puedes revisar el resultado y mostrarlo en pantalla o guardar el pago
    return JsonResponse(result)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Usuario o contraseña inválidos.')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('index')

@login_required
def profile(request):
    return render(request, 'profile.html')