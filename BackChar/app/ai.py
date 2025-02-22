import pandas as pd
from sklearn.cluster import KMeans
from app.models import Formulario
from sklearn.linear_model import LinearRegression

def prever_erros_futuros():
    # Recupera os dados da tabela Formulario
    formularios = Formulario.objects.all()

    # Cria uma lista de dicionários com os dados
    dados = []
    for formulario in formularios:
        dados.append({
            'mes': formulario.data_criacao.month,  # Mês da criação do formulário
            'erros': formulario.checklist.filter(is_checked=False).count()  # Número de erros
        })

    # Converte a lista de dicionários para um DataFrame do pandas
    df = pd.DataFrame(dados)

    # Treina um modelo de regressão linear
    model = LinearRegression()
    model.fit(df[['mes']], df['erros'])

    # Faz uma previsão para o próximo mês
    proximo_mes = df['mes'].max() + 1
    erros_previstos = model.predict([[proximo_mes]])

    return {
        'proximo_mes': proximo_mes,
        'erros_previstos': erros_previstos[0]
    }

def sugerir_treinamentos():
    # Recupera os dados da tabela Formulario
    formularios = Formulario.objects.all()

    # Cria uma lista de dicionários com os dados
    dados = []
    for formulario in formularios:
        dados.append({
            'nome': formulario.nome,
            'percentual_conclusao': formulario.percentual_conclusao,
            'erros_frequentes': formulario.checklist.filter(is_checked=False).count()
        })

    # Converte a lista de dicionários para um DataFrame do pandas
    df = pd.DataFrame(dados)

    # Usa KMeans para agrupar os funcionários com base no desempenho
    kmeans = KMeans(n_clusters=2)  # Define o número de clusters
    df['grupo'] = kmeans.fit_predict(df[['percentual_conclusao', 'erros_frequentes']])

    # Sugere treinamentos com base no grupo
    sugestoes = []
    for grupo in df['grupo'].unique():
        funcionarios = df[df['grupo'] == grupo]['nome'].tolist()
        if grupo == 0:
            sugestoes.append(f"Funcionários {funcionarios} têm bom desempenho. Sugira treinamentos avançados.")
        else:
            sugestoes.append(f"Funcionários {funcionarios} têm desempenho abaixo da média. Sugira treinamentos básicos.")

    return sugestoes