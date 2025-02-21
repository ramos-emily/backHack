from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Formulario, ChecklistItem, CSVFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import FormularioForm 
from django.db.models import Avg



@login_required
def minha_view_protegida(request):
    return render(request, 'protegida.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  # Cria o formulário de login com os dados enviados
        if form.is_valid():
            username = form.cleaned_data.get('username')  # Obtém o nome de usuário
            password = form.cleaned_data.get('password')  # Obtém a senha
            user = authenticate(username=username, password=password)  # Autentica o usuário
            if user is not None:
                login(request, user)  # Faz o login do usuário
                return redirect('home')  # Redireciona para a página inicial
    else:
        form = AuthenticationForm()  # Exibe o formulário vazio para login

    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)  # Faz o logout do usuário
    return redirect('home')  # Redireciona para a página inicial

def home(request):
    return HttpResponse("Bem-vindo à página inicial!")


class CSVUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')  # Obtém o arquivo enviado
        if file:
            CSVFile.objects.create(file=file)  # Salva o arquivo no banco de dados
            return Response({'message': 'CSV upload com sucesso!'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Nenhum arquivo enviado.'}, status=status.HTTP_400_BAD_REQUEST)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Cria o formulário de cadastro
        if form.is_valid():
            form.save()  # Salva o novo usuário no banco de dados
            username = form.cleaned_data.get('username')  # Obtém o nome de usuário
            password = form.cleaned_data.get('password1')  # Obtém a senha
            user = authenticate(username=username, password=password)  # Autentica o usuário
            login(request, user)  # Faz o login do usuário
            return redirect('home')  # Redireciona para a página inicial
    else:
        form = UserCreationForm()  # Exibe o formulário vazio para cadastro

    return render(request, 'signup.html', {'form': form})

def salvar_checklist(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id)
    
    if request.method == 'POST':
        # Itera sobre os itens do checklist relacionados ao formulário
        for item in formulario.checklist.all():
            item_id = f"item_{item.id}"
            # Verifica se o item foi marcado no formulário
            item.is_checked = item_id in request.POST
            item.save()  # Salva o status do item
        
        # Atualiza o percentual de conclusão do formulário
        formulario.atualizar_percentual_conclusao()
        
        # Redireciona de volta ao formulário após salvar
        return redirect('detalhes_formulario', formulario_id=formulario.id)

    # Renderiza o template do checklist com o formulário
    return render(request, 'detalhes_formulario.html', {'formulario': formulario})

def formulario_view(request):
    if request.method == 'POST':
        form = FormularioForm(request.POST)  # Cria o formulário com os dados enviados
        if form.is_valid():
            formulario = form.save()  # Salva o formulário e obtém a instância salva
            return redirect('salvar_checklist', formulario_id=formulario.id)  # Redireciona para a página de checklist
    else:
        form = FormularioForm()  # Exibe o formulário vazio

    # Obtém todos os itens do checklist para exibição
    checklist_itens = ChecklistItem.objects.all()

    return render(request, 'formulario.html', {'form': form, 'checklist_itens': checklist_itens})

def rendimento_equipe(request):
    formularios = Formulario.objects.all()
    media_equipe = Formulario.objects.aggregate(media_rendimento=Avg('percentual_conclusao'))['media_rendimento']
    return render(request, 'rendimento_equipe.html', {'formularios': formularios, 'media_equipe': media_equipe})

