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
    nome = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(default=timezone.now)
    checklist = models.ManyToManyField('ChecklistItem', blank=True)
    percentual_conclusao = models.FloatField(default=0.0)

    def __str__(self):
        return self.nome

    def atualizar_percentual_conclusao(self):
        # Total de itens do checklist (todos os itens existentes)
        total_itens = ChecklistItem.objects.count()

        if total_itens == 0:
            self.percentual_conclusao = 0  # Evita divisão por zero
        else:
            # Itens concluídos (marcados) no formulário
            itens_concluidos = self.checklist.filter(is_checked=True).count()
            
            # Calcula o percentual de conclusão e arredonda para 2 casas decimais
            self.percentual_conclusao = round((itens_concluidos / total_itens) * 100, 2)

        self.save()  # Salva o percentual no banco de dados

    def atualizar_percentual_conclusao(self):
        total_itens = self.checklist.count()  # Total de itens no checklist
        if total_itens == 0:
            self.percentual_conclusao = 0  # Evita divisão por zero
        else:
            itens_concluidos = self.checklist.filter(is_checked=True).count()  # Itens concluídos
            self.percentual_conclusao = (itens_concluidos / total_itens) * 100  # Calcula o percentual
        self.save()  # Salva o percentual no banco de dados