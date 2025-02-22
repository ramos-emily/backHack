from django.urls import path
from .views import (
    home, signup, user_login, user_logout, 
    CSVUploadView, formulario_view, salvar_checklist, 
    rendimento_equipe, minha_view_protegida,
)

urlpatterns = [
    path('', home, name='home'),  # Página inicial
    path('signup/', signup, name='signup'),  # Cadastro de usuário
    path('login/', user_login, name='login'),  # Login de usuário
    path('logout/', user_logout, name='logout'),  # Logout de usuário
    path('upload-csv/', CSVUploadView.as_view(), name='upload_csv'),  # Upload de CSV
    path('rendimento_equipe/', rendimento_equipe, name='rendimento_equipe'),  # Rendimento da equipe
    path('formulario/', formulario_view, name='formulario'),  # Formulário
    path('salvar_checklist/<int:formulario_id>/', salvar_checklist, name='salvar_checklist'),  # Checklist
    path('protegida/', minha_view_protegida, name='protegida'),  # Página protegida (exemplo)
    
]