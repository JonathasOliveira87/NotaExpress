from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('perfil/', views.profile_user, name='profile_user'),
    path('login/', views.login_user, name='login'),
    path('register/', views.registration, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    
    # Configure a view padrão do Django para a página de login com o nome 'login_user'
    path('login/default/', auth_views.LoginView.as_view(), name='login_user_default'),
]
