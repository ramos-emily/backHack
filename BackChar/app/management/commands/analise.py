from django.core.management.base import BaseCommand
from app.ai import sugerir_treinamentos, prever_erros_futuros

class Command(BaseCommand):
    help = 'Executa a análise de dados e sugere treinamentos e previsões'

    def handle(self, *args, **kwargs):
        sugestoes = sugerir_treinamentos()
        previsao = prever_erros_futuros()

        for sugestao in sugestoes:
            self.stdout.write(self.style.SUCCESS(sugestao))

        self.stdout.write(self.style.SUCCESS(f"Previsão de erros para o mês {previsao['proximo_mes']}: {previsao['erros_previstos']}"))