from django.db import models

class CSVFile(models.Model):
    file = models.FileField(upload_to='csv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ChecklistItem(models.Model):
    name = models.CharField(max_length=255)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Formulario(models.Model):
    nome = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    checklist = models.ManyToManyField(ChecklistItem, blank=True)

    def __str__(self):
        return self.nome
    
data_criacao = models.DateTimeField(auto_now_add=True)

