from django import forms
from .models import Formulario, ChecklistItem

class FormularioForm(forms.ModelForm):
    checklist = forms.ModelMultipleChoiceField(
        queryset=ChecklistItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Formulario
        fields = ['nome', 'checklist']


data_criacao = forms.DateTimeField(
    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    required=True
)
