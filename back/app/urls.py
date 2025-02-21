from django.urls import path
from .views import home, signup, user_login, user_logout, CSVUploadView, formulario_view, salvar_checklist, rendimento_equipe
from . import views


urlpatterns = [
    path('', home, name='home'),  # Rota para a página inicial
    path('signup/', signup, name='signup'),  # Rota para o cadastro
    path('login/', user_login, name='login'),  # Rota para o login
    path('logout/', user_logout, name='logout'),  # Rota para o logout
    path('upload-csv/', CSVUploadView.as_view(), name='upload_csv'),  # Rota para o upload de CSV
    path('rendimento_equipe/', rendimento_equipe, name='rendimento_equipe'),
    path('formulario/', formulario_view, name='formulario'),
    path('salvar_checklist/<int:formulario_id>/', salvar_checklist, name='salvar_checklist'),
    
]