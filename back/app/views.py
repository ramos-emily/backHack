from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CSVFile
from .forms import FormularioForm

def formulario_view(request):
    if request.method == 'POST':
        form = FormularioForm(request.POST)
        if form.is_valid():  # Valida o formulário
            form.save()  # Salva no banco
            return redirect('formulario')  # Redireciona após o sucesso
    else:
        form = FormularioForm()

    return render(request, 'formulario.html', {'form': form})

#CSV do gamemaker
class CSVUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if file:
            CSVFile.objects.create(file=file)
            return Response({'message': 'CSV upload com sucesso!'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Nenhum arquivo enviado.'}, status=status.HTTP_400_BAD_REQUEST)

# View de cadastro (signup)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial após o cadastro
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# View de login (user_login)
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redireciona para a página inicial após o login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# View de logout (user_logout)
def user_logout(request):
    logout(request)
    return redirect('home')  # Redireciona para a página inicial após o logout

# View de home (home)
def home(request):
    return HttpResponse("Bem-vindo à página inicial!")
