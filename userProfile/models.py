from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='fotoUsuario/')

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = 'Perfil do Usuário'