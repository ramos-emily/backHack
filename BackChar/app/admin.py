from django.contrib import admin
from .models import Formulario, ChecklistItem  # Importe os modelos

# Registre o modelo Formulario
@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_criacao', 'percentual_conclusao')  # Campos exibidos na lista
    search_fields = ('nome',)  # Campos pesquisáveis
    list_filter = ('data_criacao',)  # Filtros laterais

# Registre o modelo ChecklistItem (se já não estiver registrado)
@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'is_checked')  # Campos exibidos na lista
    search_fields = ('descricao',)  # Campos pesquisáveis