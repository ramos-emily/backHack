from django.urls import path
from .views import home, signup, user_login, user_logout, CSVUploadView, formulario_view

urlpatterns = [
    path('', home, name='home'),  # Página inicial
    path('signup/', signup, name='signup'),  # Cadastro
    path('login/', user_login, name='login'),  # Login
    path('logout/', user_logout, name='logout'),  # Logout
    path('api/upload-csv/', CSVUploadView.as_view(), name='upload-csv'),
    path('formulario/', formulario_view, name='formulario'),
]
