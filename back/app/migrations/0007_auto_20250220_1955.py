from django.db import migrations

def atualizar_nomes(apps, schema_editor):
    ChecklistItem = apps.get_model('app', 'ChecklistItem') 
    for item in ChecklistItem.objects.all():
        item.name = f"Item {item.id}"  # Defina um valor significativo
        item.save()

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0006_auto_20250220_1955'),  # Mantenha a dependência gerada
    ]

    operations = [
        migrations.RunPython(atualizar_nomes),  # Adicione a operação de migração
    ]