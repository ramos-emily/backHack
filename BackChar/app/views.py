from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Formulario, ChecklistItem, CSVFile
from .forms import FormularioForm
from django.db.models import Avg
from app.models import Formulario
import pandas as pd
from .ai import sugerir_treinamentos, prever_erros_futuros

def analise_view(request):
    # Chama as funções de IA
    sugestoes = sugerir_treinamentos()
    previsao = prever_erros_futuros()

    # Renderiza o template com os dados
    return render(request, 'analise.html', {
        'sugestoes': sugestoes,
        'previsao': previsao
    })

def exportar_csv(request):
    # Consulta os dados da tabela Formulario
    formularios = Formulario.objects.all()

    # Cria uma lista de dicionários com os dados
    dados = []
    for formulario in formularios:
        for item in formulario.checklist.all():
            dados.append({
                'nome': formulario.nome,
                'percentual_conclusao': formulario.percentual_conclusao,
                'data_criacao': formulario.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
                'checklist_descricao': item.descricao,
                'checklist_is_checked': item.is_checked
            })

    # Converte a lista de dicionários para um DataFrame do pandas
    df = pd.DataFrame(dados)

    # Cria uma resposta HTTP com o arquivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="formularios_checklist.csv"'

    # Salva o DataFrame no response
    df.to_csv(response, index=False)

    return response

# Página inicial
def home(request):
    return HttpResponse("Bem-vindo à página inicial!")

# Cadastro de usuário
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login de usuário
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout de usuário
def user_logout(request):
    logout(request)
    return redirect('home')

# Upload de CSV (API)
class CSVUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if file:
            CSVFile.objects.create(file=file)
            return Response({'message': 'CSV upload com sucesso!'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Nenhum arquivo enviado.'}, status=status.HTTP_400_BAD_REQUEST)

# Formulário e Checklist
def formulario_view(request):
    if request.method == 'POST':
        form = FormularioForm(request.POST)
        if form.is_valid():
            # Cria um novo formulário com o nome do funcionário
            formulario = form.save()

            # Associa os itens do checklist marcados ao formulário
            for item in ChecklistItem.objects.all():
                item_id = f"item_{item.id}"
                if item_id in request.POST:
                    formulario.checklist.add(item)

            # Atualiza o percentual de conclusão
            formulario.atualizar_percentual_conclusao()

            # Redireciona para a página de detalhes do formulário
            return redirect('salvar_checklist', formulario_id=formulario.id)
    else:
        form = FormularioForm()

    # Recupera todos os itens do checklist para exibição no formulário
    checklist_itens = ChecklistItem.objects.all()
    return render(request, 'formulario.html', {'form': form, 'checklist_itens': checklist_itens})

def salvar_checklist(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id)

    if request.method == 'POST':
        # Atualiza os itens do checklist com base no que foi marcado
        for item in formulario.checklist.all():
            item_id = f"item_{item.id}"
            item.is_checked = item_id in request.POST
            item.save()

        # Atualiza o percentual de conclusão
        formulario.atualizar_percentual_conclusao()

        # Redireciona para a página de detalhes do formulário
        return redirect('salvar_checklist', formulario_id=formulario.id)

    return render(request, 'detalhes_formulario.html', {'formulario': formulario})

# Rendimento da Equipe
def rendimento_equipe(request):
    formularios = Formulario.objects.all()
    media_equipe = Formulario.objects.aggregate(media_rendimento=Avg('percentual_conclusao'))['media_rendimento']
    return render(request, 'rendimento_equipe.html', {
        'formularios': formularios,
        'media_equipe': media_equipe
    })

# Página protegida (exemplo)
@login_required
def minha_view_protegida(request):
    return render(request, 'protegida.html')