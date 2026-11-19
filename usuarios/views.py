
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def login_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=email,
            password=password
        )

        if usuario is not None:
            login(request, usuario)
            return redirect('inicio')

        return render(request, 'usuarios/login.html', {
            'error': 'Correo o contrasena incorrectos.'
        })

    return render(request, 'usuarios/login.html')


def inicio_view(request):

    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'usuarios/inicio.html', {
        'rol': request.user.role
    })

def logout_view(request):
    logout(request)
    return redirect('login')
