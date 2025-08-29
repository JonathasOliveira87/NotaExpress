from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from core.context_global import pic_global
from .models import UserProfile
User = get_user_model()


@login_required
def profile_user(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:

        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'GET':
        return render(request, 'userProfile.html', pic_global(request))
    else:
        form_type = request.POST.get('form_type')
        if form_type == 'update_email':
            user = request.user
            new_email = request.POST.get('new_email')
            confirm_email = request.POST.get('confirm_email')
            if new_email == confirm_email:
                user.email = new_email
                user.save()
                messages.success(request, 'E-mail atualizado com sucesso!')
            else:
                messages.error(request, 'Os e-mails não correspondem.')

        elif form_type == 'update_password':
            user = request.user
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                if check_password(current_password, user.password):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Senha atualizada com sucesso!')
                else:
                    messages.error(request, 'Senha atual incorreta.')
            else:
                messages.error(request, 'Erro de dados: as senhas não correspondem.')

        elif form_type == 'update_photo':
            user_profile = UserProfile.objects.get(user=request.user)
            photo = request.FILES.get('update_photo')  # Obtém o arquivo enviado pelo campo de entrada de arquivo
        
            if photo:  # Verifica se um arquivo foi enviado
                user_profile.profile_pic = photo
                user_profile.save()
                messages.success(request, 'Foto atualizado com sucesso!')
    return render(request, 'userProfile.html', pic_global(request))


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if user is not None and user.check_password(password):
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Logado com sucesso!')
                    #check_new_messages(request)
                    return redirect('/')
                else:
                    messages.error(request, 'Sua conta está inativa. Entre em contato com o administrador.')
            else:
                messages.error(request, 'Nome de usuário ou senha incorretos.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')

    return render(request, 'login.html')


@login_required 
def logout_user(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso. Até logo!')
    return redirect( '/')


def registration(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        if request.user.is_authenticated:
            messages.warning(request, 'Você já está logado!')
            return redirect('/')

        username = request.POST.get('username')
        email = request.POST.get('email')
        confirmEmail = request.POST.get('confirm-email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirm-password')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')

        new_user = User.objects.filter(username=username)

        if new_user.exists():
            messages.error(request, 'Nome de usuário já existe!')
            return render(request, 'register.html')
        
        if password != confirmPassword:
            messages.error(request, 'As senhas não conferem!')
            return render(request, 'register.html')
        
        if email != confirmEmail:
            messages.error(request, 'O Email não conferem!')
            return render(request, 'register.html')

        # Crie o usuário com create_user()
        new_user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)

    

        # Criação do perfil de usuário
        user_profile = UserProfile(user=new_user)
        user_profile.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('/perfil/')
