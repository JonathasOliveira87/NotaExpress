from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Movimentacao, categoriaProduto, LocalProduto
from django.contrib import messages
from decimal import Decimal
import re
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from core.context_global import pic_global


@login_required
#@permission_required('app.create', raise_exception=True)
def create(request):
    context = pic_global(request)
    if not request.user.groups.filter(name='Almoxarifado').exists():
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    categorias = categoriaProduto.objects.all()
    local = LocalProduto.objects.all()

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nome = request.POST.get('nome')
        nome_fornecedor = request.POST.get('nomeForn')
        quantidade = request.POST.get('quantidade')
        preco = request.POST.get('preco', '').replace('R$', '').replace(',', '').replace('.', '')
        foto_produto = request.FILES.get('update_photo')

        categoria_id = request.POST.get('categoria')
        categoria = get_object_or_404(categoriaProduto, id=categoria_id)

        local_id = request.POST.get('local')
        local = get_object_or_404(LocalProduto, id=local_id)

        # Remover caracteres não numéricos e não ponto
        preco = re.sub(r'[^0-9.]', '', preco)

        try:
            preco = Decimal(preco) / 100  # Divida por 100 se estiver trabalhando com centavos
        except Exception as e:
            print(f"Erro ao converter o preço: {e}")
            pass



        try:
            Produto.objects.create(
                codigo=codigo,
                nome=nome,
                quantidade=quantidade,
                local_produto=local,
                preco=preco,
                nome_fornecedor=nome_fornecedor,
                categoria_produto=categoria,
                foto_produto=foto_produto
            )
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('cadProduto')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar produto: {e}')

    return render(request, 'cadastrarProduto.html', {'categorias': categorias, 'local' : local, **context})


@login_required
def listar_produtos(request):
    context = pic_global(request)
    produtos = Produto.objects.all()
    # Verifica se houve uma solicitação de pesquisa
    query = request.GET.get('qProduto')
    if query:
        produtos = produtos.filter(nome__icontains=query)
        if not produtos.exists():
            messages.info(request, 'Nenhum produto encontrado com esse nome.')
            return redirect('verEstoque')
        
    return render(request, 'verEstoque.html', {'produtos': produtos, **context})


@login_required
def detalhes_produto(request, id):
    context = pic_global(request)
    categorias = categoriaProduto.objects.all()
    produto = Produto.objects.get(id=id)
    local = LocalProduto.objects.all()
    return render(request, 'infoProduto.html', {'produto': produto, 'local' : local, 'categorias': categorias, **context})


@login_required
def update(request, id):
    context = pic_global(request)
    categorias = categoriaProduto.objects.all()
    local = LocalProduto.objects.all()
    produto = Produto.objects.get(id=id)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        nome_fornecedor = request.POST.get('nomeForn')
        quantidade = request.POST.get('quantidade')
        preco = request.POST.get('preco', '').replace('R$', '').replace(',', '').replace('.', '')

        foto_produto = request.FILES.get('update_photo')

        # Remover caracteres não numéricos e não ponto
        preco = re.sub(r'[^0-9.]', '', preco)

        try:
            preco = Decimal(preco) / 100  # Divida por 100 se estiver trabalhando com centavos
        except Exception as e:
            print(f"Erro ao converter o preço: {e}")
            pass

        categoria_id = request.POST.get('categoria')  # Certifique-se de que o nome do campo é o correto
        categoria = get_object_or_404(categoriaProduto, id=categoria_id)
        

        try:
            produto.nome = nome
            produto.quantidade = quantidade
            produto.preco=preco
            produto.nome_fornecedor = nome_fornecedor
            produto.categoria_produto = categoria
            if foto_produto != None:
                produto.foto_produto = foto_produto
            produto.save()

            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('verEstoque')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar produto: {e}')

    return render(request, 'editarProduto.html', {'produto': produto, 'local' : local, 'categorias': categorias, **context})



@login_required
def ver_produto(request, id):
    context = pic_global(request)
    categorias = categoriaProduto.objects.all()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        nome_fornecedor = request.POST.get('nomeForn')
        quantidade = request.POST.get('quantidade')
        preco = request.POST.get('preco', '').replace('R$', '').replace(',', '').replace('.', '')

        foto_produto = request.FILES.get('update_photo')

        # Remover caracteres não numéricos e não ponto
        preco = re.sub(r'[^0-9.]', '', preco)

        try:
            preco = Decimal(preco) / 100  # Divida por 100 se estiver trabalhando com centavos
        except Exception as e:
            print(f"Erro ao converter o preço: {e}")
            pass

        categoria_id = request.POST.get('categoria')  # Certifique-se de que o nome do campo é o correto
        categoria = get_object_or_404(categoriaProduto, id=categoria_id)
        produto = Produto.objects.get(id=id)

        try:
            produto.nome = nome
            produto.quantidade = quantidade
            produto.preco=preco
            produto.nome_fornecedor = nome_fornecedor
            produto.categoria_produto = categoria
            if foto_produto != None:
                produto.foto_produto = foto_produto
            produto.save()

            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('verEstoque')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar produto: {e}')

    return render(request, 'infoProduto.html', {'produto': produto, 'categorias': categorias, **context})