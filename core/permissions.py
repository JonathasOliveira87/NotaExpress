from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from note.models import cNota

def criar_permissao():
    content_type = ContentType.objects.get_for_model(cNota)

    # Crie a permissão
    permission = Permission.objects.create(
        codename='app.criar_nota',
        name='Criar Nota',
        content_type=content_type,
    )

    # Associe a permissão ao grupo "Operador"
    group = Group.objects.get(name='Almoxarifado')
    group.permissions.add(permission)
