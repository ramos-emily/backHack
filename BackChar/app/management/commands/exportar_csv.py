import pandas as pd
from django.core.management.base import BaseCommand
from app.models import Formulario

class Command(BaseCommand):
    help = 'Exporta os dados da tabela Formulario e ChecklistItem para um arquivo CSV'

    def handle(self, *args, **kwargs):
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

        # Salva o DataFrame como um arquivo CSV
        df.to_csv('formularios_checklist.csv', index=False)

        self.stdout.write(self.style.SUCCESS('Dados exportados com sucesso para formularios_checklist.csv'))