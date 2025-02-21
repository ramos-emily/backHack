from django.db import models
from django.utils import timezone  # Importe timezone para definir um valor padrão

class CSVFile(models.Model):
    file = models.FileField(upload_to='csv/')  # Campo para upload de arquivos CSV
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Data e hora do upload

    def __str__(self):
        return f"Arquivo CSV {self.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


from django.db import models

class ChecklistItem(models.Model):
    descricao = models.CharField(max_length=255, default="Descrição Padrão")  # Valor padrão para o campo 'descricao'
    is_checked = models.BooleanField(default=False)  # Status do item (marcado/não marcado)

    def __str__(self):
        return self.descricao


class Formulario(models.Model):
    nome = models.CharField(max_length=100)  # Nome do formulário
    data_criacao = models.DateTimeField(default=timezone.now)  # Campo renomeado
    checklist = models.ManyToManyField('ChecklistItem', blank=True)  # Relação com ChecklistItem

    def __str__(self):
        return self.nome

    @property
    def percentual_conclusao(self):
        """
        Calcula o percentual de conclusão do checklist.
        """
        total_itens = self.checklist.count()  # Total de itens no checklist
        if total_itens == 0:
            return 0  # Evita divisão por zero

        itens_concluidos = self.checklist.filter(is_checked=True).count()  # Itens marcados como concluídos
        return (itens_concluidos / total_itens) * 100  # Retorna o percentual
