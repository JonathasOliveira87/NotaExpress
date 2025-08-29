from django.shortcuts import render, redirect, get_object_or_404
from .models import cNota, selectSetor, OrdemServico
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from manageStock.models import categoriaProduto, Produto
import json
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from core.context_global import pic_global
from django.http import JsonResponse

import plotly.express as px
import plotly.graph_objects as go
from django.db.models import Count


@login_required
def criarNota(request):
    if not request.user.groups.filter(name='Operador').exists():
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    setores = selectSetor.objects.all()
    context = pic_global(request)
    if request.method == 'POST':
        titulo = request.POST.get('title')
        setor_id = request.POST.get('opcoes')
        descricao = request.POST.get('cnota')
        data_criacao = request.POST.get('data_criacao')
        tag = request.POST.get('tag')

        try:
            # Converta a string da data para um objeto datetime
            data_criacao = datetime.strptime(data_criacao, '%Y-%m-%dT%H:%M')
            data_criacao = timezone.make_aware(data_criacao)
            # Converta o ID do setor para um objeto selectSetor
            setor = selectSetor.objects.get(id=int(setor_id))
            descricao = request.POST.get('cnota')

            nova_nota = cNota.objects.create(titulo=titulo, setor=setor, descricao=descricao, data_criacao=data_criacao, tag=tag, criado_por=request.user)
            nova_nota.save()
            messages.success(request, 'Nota criada com sucesso!')
            return redirect('criarNota')
        except selectSetor.DoesNotExist:
            messages.error(request, 'Setor não encontrado.')
        except ValueError:
            messages.error(request, 'ID do setor inválido.')
        except Exception as e:
            messages.error(request, f'Erro ao criar a nota: {e}')

    return render(request, 'criarNota.html', {'setores': setores, **context})


@login_required
def listarNotas(request):
    context = pic_global(request)
    notas = cNota.objects.all()
    # Verifica se houve uma solicitação de pesquisa
    query = request.GET.get('qNota')
    if query:
        # Remove os zeros à esquerda da consulta
        query = query.lstrip('0')
        # Filtra as notas com base no número da nota (sem zeros à esquerda)
        notas = notas.filter(numero__icontains=query)
        # Verifica se existem notas encontradas
        if not notas.exists():
            messages.info(request, f'Nenhuma nota encontrada para a consulta {query} !')
            return redirect('listarNota')

    # Retorna a mesma página mesmo que não existam notas encontradas
    return render(request, 'listarNota.html', {'notas': notas, **context})


@login_required
def detalhesNota(request, ver_nota):
    context = pic_global(request)
    categorias = categoriaProduto.objects.all()
    nota = get_object_or_404(cNota, numero=ver_nota)
    produtos = Produto.objects.all()
    return render(request, 'infoNota.html', {'nota': nota, 'categorias': categorias, 'produtos': produtos, **context})


@login_required
def criarOrdem(request):
    context = pic_global(request)
    if request.method == 'POST':
        try:
            # Recuperar os dados do formulário
            hora_inicio = request.POST.get('hinicio')
            hora_fim = request.POST.get('hfim')
            total_horas_str = request.POST.get('totalHoras')
            quantidade_estoque = request.POST.get('quantidade')
            itens_requisitados = json.loads(request.POST.get('itensRequisitados'))
            itens_requisitados_json = json.dumps(itens_requisitados)
            preco_total = request.POST.get('precoTotal')
            id_nota = request.POST.get('id_nota')
            #id_produtos = request.POST.getlist('id_produto[]')
            id_produtos = [int(id_produto) for id_produto in request.POST.getlist('id_produto[]')]

            # Obtém a nota associada à ordem de serviço 
            nota_associada = cNota.objects.get(numero=id_nota)

            # Criar a ordem de serviço no banco de dados
            ordem_servico = OrdemServico.objects.create(
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                total_horas=total_horas_str,
                itens_requisitados=itens_requisitados_json,
                preco_total=preco_total,
                orderm_criado_por=request.user,
                nota=nota_associada,  # Passa a nota associada à ordem de serviço
            )

            if quantidade_estoque is not None and quantidade_estoque != '':
                # Converter as quantidades de produtos para uma lista de inteiros
                quantidades = json.loads(quantidade_estoque)

                print("Quantidade de Estoque:", quantidades)
                print("Itens Requisitados:", itens_requisitados)
                print("IDs dos Produtos:", id_produtos)

                for id_produto, quantidade in zip(id_produtos, quantidades):
                    try:
                        # Obtém o produto associado à ordem de serviço 
                        produto_associado = Produto.objects.get(codigo=id_produto)
                        # Atualiza a quantidade de produtos no estoque
                        produto_associado.quantidade = quantidade
                        produto_associado.save()
                        # Associa o produto à ordem de serviço

                        ordem_servico.save()
                    except Exception as e:
                        # Se ocorrer outra exceção, registre um erro
                        messages.error(request, f"Ocorreu um erro ao processar o produto com código {id_produto}: {str(e)}")
            messages.success(request, 'Ordem criada com sucesso!')
            return redirect('listarOrdem')

        except ValidationError as e:
            # Tratar a exceção ValidationError aqui
            error_message = f"Erro de validação: {e.message}"
            messages.error(request, error_message)
            return render(request, 'infoNota.html', {'error_message': error_message, **context})

        except Exception as e:
            # Capturar exceções não especificadas
            error_message = f"Ocorreu um erro inesperado: {str(e)}"
            messages.error(request, error_message)
            return render(request, 'infoNota.html', {'error_message': error_message, **context})

    else:
        # Caso seja um GET, você pode retornar uma resposta renderizada para exibir um formulário vazio ou fazer qualquer outra coisa necessária
        return render(request, 'infoNota.html')


@login_required
def listarOrdens(request):
    context = pic_global(request)
    ordens = OrdemServico.objects.all()
    # Verifica se houve uma solicitação de pesquisa
    query = request.GET.get('qOrdem')
    if query:
        # Filtra as notas com base no número da nota (sem zeros à esquerda)
        ordens = ordens.filter(id_hexadecimal__icontains=query)
        # Verifica se existem notas encontradas
        if not ordens.exists():
            messages.info(request, f'Nenhuma ordem encontrada para a consulta {query}!')
            return redirect('listarOrdem')

    # Retorna a mesma página mesmo que não existam ordens encontradas
    return render(request, 'listarOrdem.html', {'ordens': ordens, **context})


@login_required
def detalhesOrdem(request, ver_ordem):
    context = pic_global(request)
    ordem = get_object_or_404(OrdemServico, id_hexadecimal=ver_ordem)

    # Obtenha a nota associada a esta ordem
    nota_associada = ordem.nota

    # Convertendo a string JSON em um objeto Python
    ordem.itens_requisitados = json.loads(ordem.itens_requisitados)

    return render(request, 'infoOrdem.html', {'nota': nota_associada, 'ordem': ordem, **context})

@login_required
def atualizar_status_ordem(request):
    context = pic_global(request)
    ordens = OrdemServico.objects.all()
    
    if request.method == 'POST':
        try:
            if 'encerrar_ordem_id' in request.POST:
                ordem_id = request.POST.get('encerrar_ordem_id')
                novo_status = 'encerrado'
                # Obtenha a ordem de serviço com base no ID
                ordem = OrdemServico.objects.get(pk=ordem_id)
                # Atualize o status da ordem
                ordem.status = novo_status
                ordem.encerrado_por = request.user
                ordem.save()
                messages.success(request, 'Ordem ENCERRADO com sucesso!')
            elif 'finalizar_ordem_id' in request.POST:
                ordem_id = request.POST.get('finalizar_ordem_id')
                novo_status = 'finalizado'
                # Obtenha a ordem de serviço com base no ID
                ordem = OrdemServico.objects.get(pk=ordem_id)
                # Atualize o status da ordem
                ordem.status = novo_status
                ordem.finalizado_por = request.user
                ordem.save()
                messages.success(request, 'Ordem FINALIZADA com sucesso!')
        except OrdemServico.DoesNotExist:
            messages.error(request, 'Ordem não encontrada.')
        except Exception as e:
            # Capturar exceções não especificadas
            error_message = f"Ocorreu um erro inesperado: {str(e)}"
            messages.error(request, error_message)
            return render(request, 'infoNota.html', {'error_message': error_message, **context})
        
    return render(request, 'listarOrdem.html', {'ordens': ordens, **context})

@login_required
def finalizar_ordem(request):
    context = pic_global(request)
    ordens = OrdemServico.objects.all()
    if request.method == 'POST':
        try:
            if 'finalizar_ordem_id' in request.POST:
                ordem_id = request.POST.get('finalizar_ordem_id')
                novo_status = 'finalizado'
                # Obtenha a ordem de serviço com base no ID
                ordem = OrdemServico.objects.get(pk=ordem_id)
                # Atualize o status da ordem
                ordem.status = novo_status
                ordem.finalizado_por = request.user
                ordem.save()
                messages.success(request, 'Ordem FINALIZADA com sucesso!')
        except OrdemServico.DoesNotExist:
            messages.error(request, 'Ordem não encontrada.')
        except Exception as e:
            # Capturar exceções não especificadas
            error_message = f"Ocorreu um erro inesperado: {str(e)}"
            messages.error(request, error_message)
            return render(request, 'infoNota.html', {'error_message': error_message, **context})
        
    return render(request, 'listarOrdem.html', {'ordens': ordens, **context})

@login_required
def encerrar_ordem(request):
    context = pic_global(request)
    ordens = OrdemServico.objects.all()
    if request.method == 'POST':
        try:
            if 'encerrar_ordem_id' in request.POST:
                ordem_id = request.POST.get('encerrar_ordem_id')
                novo_status = 'encerrado'
                # Obtenha a ordem de serviço com base no ID
                ordem = OrdemServico.objects.get(pk=ordem_id)
                # Atualize o status da ordem
                ordem.status = novo_status
                ordem.encerrado_por = request.user
                ordem.save()
                messages.success(request, 'Ordem ENCERRADO com sucesso!')
        except OrdemServico.DoesNotExist:
            messages.error(request, 'Ordem não encontrada.')
        except Exception as e:
            # Capturar exceções não especificadas
            error_message = f"Ocorreu um erro inesperado: {str(e)}"
            messages.error(request, error_message)
            return render(request, 'infoNota.html', {'error_message': error_message, **context})
        
    return render(request, 'listarOrdem.html', {'ordens': ordens, **context})


def dashboard(request):
    # Consultar o banco de dados Django para obter as notas
    notas = cNota.objects.all()
    #ordens = OrdemServico.objects.all()

    context = pic_global(request)
    # Preparar os dados para o gráfico
    fechadas = notas.filter(fechada=True).count()
    abertas = notas.filter(fechada=False).count()
    #status_counts = ordens.values('status').annotate(total=Count('status'))

    # Definir cores específicas para cada categoria
    colorsBar = {'Abertas': 'red', 'Concluídas': 'Green'}

    '''# Definir cores específicas para cada categoria das ordens de serviço
    colors_ordens = {
        'aberto': 'red',
        'programado': 'blue',
        'encerrado': 'green',
        'finalizado': 'purple'
    }'''


    # Criar o gráfico de barras com cores especificadas
    fig_nota_bar = px.bar(
        x=['Abertas', 'Concluídas'], 
        y=[abertas, fechadas],
        color=['Abertas', 'Concluídas'],
        color_discrete_map=colorsBar,  # Mapeamento das cores para cada categoria
        title='DashBoard de notas abertas e concluídas em barras',
        labels={'x': 'Notas', 'y':'Total de notas'}
    )

    # Criar o gráfico de pizza com o Plotly Graph Objects
    fig_nota_pie = go.Figure(data=[go.Pie(
        labels=['Abertas', 'Concluídas'],
        values=[abertas, fechadas],
        hole=0,                 # Tamanho do buraco no centro do gráfico
        pull=[0, 0.1],       # Recuo das fatias (primeira fatia sem recuo, segunda fatia com 20% de recuo)
        marker=dict(colors=['red', 'green']),  # Cores das fatias
        title='DashBoard de notas abertas e concluídas em pizza',  # Título do gráfico
        textinfo='percent+label',  # Informações exibidas nas fatias
        insidetextorientation='radial',  # Orientação do texto dentro das fatias
    )])

        # Criar o gráfico de barras das ordens de serviço
    '''fig_ordens_bar = px.bar(
        x=[status['status'] for status in status_counts],
        y=[status['total'] for status in status_counts],
        color=[status['status'] for status in status_counts],
        color_discrete_map=colors_ordens,
        title='Distribuição de Ordens de Serviço por Status',
        labels={'x': 'Status', 'y': 'Total de Ordens'}
    )'''

    dashboardNota = fig_nota_bar.to_html()
    dashboardNotaPie = fig_nota_pie.to_html()
    #dashboardOrdem = fig_ordens_bar.to_html()

    

    return render(request, 'dash.html', {'dashboardNota': dashboardNota, 'dashboardNotaPie': dashboardNotaPie, **context})