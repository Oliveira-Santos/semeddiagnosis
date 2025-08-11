from django.conf import settings
import json
import csv
from django.contrib.auth import authenticate, login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import CustomUser  # Certifique-se de importar o modelo CustomUser
from django.views import View
from .forms import CSVUploadForm
from .models import Habilidade
from io import TextIOWrapper
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .models import DiagnoseInicProfPort, DiagnoseMatematicaProf, DiagnoseAnosFinaisProfPort, DiagnoseAlunoPortugues,DiagnoseAlunoMatematica
import pandas as pd
from django.http import JsonResponse
from .models import DiagnoseAnosFinaisProfMat
import mimetypes
from .models import Professor,Aluno,HabilidadeMatematica, HabilidadePortugues
from itertools import groupby
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm  # Supondo que você tenha um form personalizado

from .models import Suporte, Feedback
from .forms import SuporteForm, FeedbackForm

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .processar_planilha import processar_planilha
from .processar_planilha import processar_csv_e_salvar_no_banco
from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render, redirect
from .models import Registro  # Substitua com o modelo correto
from .forms import RegistroForm  # Certifique-se de que existe um formulário correspondente

from .models import Registro

from django.shortcuts import render
from .processar_planilha import processar_csv_e_salvar_no_banco
import os

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from webapp.models import Registro

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

from django.utils.timezone import now

from django.templatetags.static import static  # Import static utility

from datetime import datetime

from pathlib import Path
from django.utils.timezone import now
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.shortcuts import get_object_or_404
from django.conf import settings

import os
from django.conf import settings
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.utils.timezone import now
from pathlib import Path
from django.conf import settings

from pathlib import Path
from django.conf import settings
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors






# Use o modelo de usuário personalizado
User = get_user_model()



# =============================================
# Lógica de usuários e base
# =============================================

def BASE(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirecione para a página de login após o registro
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_superuser(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            
            # Criar o superusuário
            user = User.objects.create_superuser(username=username, email=email, password=password)
            user.save()
            messages.success(request, f'Super usuário {username} criado com sucesso!')
            return redirect('admin:index')
        
        return render(request, 'create_superuser.html')
    else:
        messages.error(request, 'Você não tem permissão para criar um superusuário.')
        return redirect('login')
    
@login_required
def base_view(request):
    return render(request, 'base.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Registro, CustomUser  # seu usuário admin
from django.contrib.auth.hashers import check_password

def custom_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        senha = request.POST.get('password')
        user_type = request.POST.get('user_type')

        # === LOGIN PARA CANDIDATO ===
        if user_type == 'candidato':
            try:
                candidato = Registro.objects.get(cpf=cpf)
                if check_password(senha, candidato.senha):
                    request.session['candidato_id'] = candidato.id
                    return redirect('painel_candidato')
                else:
                    messages.error(request, 'Senha incorreta para candidato.')
            except Registro.DoesNotExist:
                messages.error(request, 'CPF de candidato não encontrado.')
            return render(request, 'login.html')

        # === LOGIN PARA ADMIN OU OUTROS ===
        try:
            user = CustomUser.objects.get(email=email, cpf=cpf)
            if user.check_password(senha):
                login(request, user)  # login do Django
                return redirect('dashboard')  # redireciona para dashboard dos admins
            else:
                messages.error(request, 'Senha incorreta para administrador.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Usuário administrador não encontrado.')

    return render(request, 'login.html')



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')  # Redirecionar para a página de login após o logout
    
def custom_logout_view(request):
    logout(request)
    return render(request, 'logout.html')


# =================================================
# Modelos de Português Anos Iniciais Professores
# ==================================================

def lingua_portuguesa_prof_view(request):
    # Lista de turmas (salas de aula) que serão usadas para analisar as respostas dos professores.
    turmas = [
        '401', '403', '404', '406', '408', '409', '410', '413', '414', '415', '417',
        '421', '423', '426', '428', '429', '430', '431', '432', '433', '434', '435',
        '436', '437', '438', '439', '441', '442', '447', '451', '471'
    ]
    
    # Lista para armazenar os itens e as respostas associadas.
    itens = []

    # Variáveis para armazenar as contagens de respostas corretas e erradas.
    total_corretas = 0
    total_erradas = 0
    total_respostas = 0  # Variável para armazenar o total de respostas analisadas.

    # Recupera todos os itens do banco de dados para a tabela DiagnoseInicProfPort.
    itens_db = DiagnoseInicProfPort.objects.all()

    # Itera sobre cada item recuperado do banco de dados.
    for item in itens_db:
        # Dicionário para armazenar as respostas de cada turma para o item específico.
        respostas = {}
        
        # Para cada turma, recupera a resposta associada.
        for turma in turmas:
            resposta = getattr(item, f'professor_{turma}', 'N')  # Obtém a resposta para a turma, se não existir, retorna 'N' (Nenhuma resposta).
            respostas[turma] = resposta  # Armazena a resposta no dicionário de respostas.
            
            # Incrementa a contagem de respostas corretas ou erradas com base na resposta.
            if resposta == 'S':  # Se a resposta for 'S', considera correta.
                total_corretas += 1
            else:  # Caso contrário, considera como errada.
                total_erradas += 1
            total_respostas += 1  # Incrementa o total de respostas processadas.

        # Adiciona as informações do item e suas respostas na lista de itens.
        itens.append({
            'numero': item.item,  # Número do item.
            'habilidade': item.habilidade,  # Habilidade associada ao item.
            'descricao_habilidade': item.descricao_habilidade,  # Descrição da habilidade (se disponível).
            'respostas': respostas  # Respostas de todas as turmas para este item.
        })

    # Calcula o percentual de acertos.
    percentual_acertos = (total_corretas / total_respostas) * 100 if total_respostas > 0 else 0
    
    # Calcula o percentual de erros.
    percentual_erros = (total_erradas / total_respostas) * 100 if total_respostas > 0 else 0

    uploaded_file_url = None  # Inicializa a variável para armazenar a URL do arquivo carregado, caso exista.

    # Se o método da requisição for POST, significa que o usuário está enviando dados.
    if request.method == 'POST':
        # Verifica se o formulário de upload da planilha foi submetido.
        if 'upload_planilha' in request.POST and request.FILES.get('planilha'):
            # Recupera o arquivo da planilha submetido.
            planilha = request.FILES['planilha']
            
            # Armazena o arquivo usando o FileSystemStorage.
            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)  # Obtém a URL do arquivo carregado para exibição.

            try:
                # Usa o Pandas para ler o arquivo Excel.
                df = pd.read_excel(fs.path(filename))

                # Itera sobre as linhas do DataFrame para processar cada item e habilidade.
                for index, row in df.iterrows():
                    item_num = row['Item']  # Número do item.
                    habilidade = row['Habilidade']  # Nome da habilidade.

                    # Cria ou atualiza o item no banco de dados.
                    diagnose, created = DiagnoseInicProfPort.objects.get_or_create(
                        item=item_num,
                        habilidade=habilidade
                    )

                    # Itera sobre cada turma para salvar as respostas.
                    for turma in turmas:
                        resposta = row.get(str(turma), 0)  # Obtém a resposta da turma, com valor padrão '0'.
                        # Define a resposta como 'S' (Sim) ou 'N' (Não), com base no valor da planilha.
                        setattr(diagnose, f'professor_{turma}', 'S' if resposta == 1 else 'N')

                    diagnose.save()  # Salva o objeto no banco de dados.

                # Exibe uma mensagem de sucesso após o processamento bem-sucedido.
                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                # Caso ocorra um erro no processamento, exibe uma mensagem de erro.
                messages.error(request, f"Erro ao processar o arquivo: {e}")

            # Redireciona o usuário para a mesma página após o upload.
            return redirect('lingua_portuguesa_prof_view')

        # Verifica se o formulário para salvar as respostas foi submetido.
        if 'salvar_respostas' in request.POST:
            # Itera sobre os itens para salvar as novas respostas.
            for item in itens:
                # Recupera o item correspondente no banco de dados.
                diagnose = DiagnoseInicProfPort.objects.get(item=item['numero'])
                
                # Para cada turma, obtém a nova resposta submetida pelo usuário.
                for turma in turmas:
                    nova_resposta = request.POST.get(f'respostas_{item["numero"]}_{turma}', 'N')  # Obtém a nova resposta ou 'N' como padrão.
                    setattr(diagnose, f'professor_{turma}', nova_resposta)  # Atualiza a resposta no banco de dados.

                diagnose.save()  # Salva o objeto no banco de dados.

            # Exibe uma mensagem de sucesso após salvar as respostas.
            messages.success(request, "Respostas salvas com sucesso!")
            return redirect('lingua_portuguesa_prof_view')

    # Renderiza o template 'lingua_portuguesa_prof.html', passando as variáveis necessárias.
    return render(request, 'lingua_portuguesa_prof.html', {
        'turmas': turmas,  # Lista de turmas.
        'itens': itens,  # Lista de itens e suas respostas.
        'total_corretas': total_corretas,  # Número total de respostas corretas.
        'total_erradas': total_erradas,  # Número total de respostas erradas.
        'percentual_acertos': round(percentual_acertos, 2),  # Percentual de acertos, arredondado para 2 casas decimais.
        'percentual_erros': round(percentual_erros, 2),  # Percentual de erros, arredondado para 2 casas decimais.
        'uploaded_file_url': uploaded_file_url  # URL do arquivo carregado, se houver.
    })



def upload_excel(request):
    if request.method == "POST" and request.FILES.get("excel_file"):
        excel_file = request.FILES["excel_file"]
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            # Lê o arquivo Excel
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                Habilidade.objects.create(
                    item=row['Item'],
                    habilidade=row['Habilidade'],
                    prof_401=row['401'],
                    prof_403=row['403'],
                    prof_404=row['404'],
                    prof_406=row['406'],
                    prof_408=row['408'],
                    prof_409=row['409'],
                    prof_410=row['410'],
                    prof_413=row['413'],
                    prof_414=row['414'],
                    prof_415=row['415'],
                    prof_417=row['417'],
                    prof_421=row['421'],
                    prof_423=row['423'],
                    prof_426=row['426'],
                    prof_428=row['428'],
                    prof_429=row['429'],
                    prof_430=row['430'],
                    prof_431=row['431'],
                    prof_432=row['432'],
                    prof_433=row['433'],
                    prof_434=row['434'],
                    prof_435=row['435'],
                    prof_436=row['436'],
                    prof_437=row['437'],
                    prof_438=row['438'],
                    prof_439=row['439'],
                    prof_441=row['441'],
                    prof_442=row['442'],
                    prof_447=row['447'],
                    prof_451=row['451'],
                    prof_471=row['471']
                )
            messages.success(request, "Arquivo Excel carregado com sucesso!")
            return redirect("habilidades")
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao processar o arquivo: {e}")
            return redirect("habilidades")
    
    return render(request, "habilidades.html")


def get_diagnose_data(request):
    turmas = [
        '401', '403', '404', '406', '408', '409', '410', '413', '414', '415', '417',
        '421', '423', '426', '428', '429', '430', '431', '432', '433', '434', '435',
        '436', '437', '438', '439', '441', '442', '447', '451', '471'
    ]
    
    items = []
    for item in DiagnoseInicProfPort.objects.all():
        responses = {f"professor_{turma}": getattr(item, f"professor_{turma}", "N") for turma in turmas}
        items.append({
            "numero": item.item,
            "habilidade": item.habilidade,
            "descricao_habilidade": item.descricao_habilidade,
            "respostas": responses
        })
    
    return JsonResponse({"items": items, "turmas": turmas})


# =============================================
# Modelos de Matemática
# =============================================

def upload_habilidades2(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                # Create or update the DiagnoseMatematicaProf entry based on the 'Item' and 'Habilidade'
                diagnose, created = DiagnoseMatematicaProf.objects.get_or_create(
                    item=row['Item'],
                    habilidade=row['Habilidade']
                )

                # Update all the professor fields (300, 301, 302, etc.) based on the Excel columns
                diagnose.professor_300 = 'S' if row['300'] == 1 else 'N'
                diagnose.professor_301 = 'S' if row['301'] == 1 else 'N'
                diagnose.professor_302 = 'S' if row['302'] == 1 else 'N'
                diagnose.professor_305 = 'S' if row['305'] == 1 else 'N'
                diagnose.professor_306 = 'S' if row['306'] == 1 else 'N'
                diagnose.professor_308 = 'S' if row['308'] == 1 else 'N'
                diagnose.professor_310 = 'S' if row['310'] == 1 else 'N'
                diagnose.professor_317 = 'S' if row['317'] == 1 else 'N'
                diagnose.professor_318 = 'S' if row['318'] == 1 else 'N'
                diagnose.professor_319 = 'S' if row['319'] == 1 else 'N'
                diagnose.professor_320 = 'S' if row['320'] == 1 else 'N'
                diagnose.professor_323 = 'S' if row['323'] == 1 else 'N'
                diagnose.professor_324 = 'S' if row['324'] == 1 else 'N'
                diagnose.professor_328 = 'S' if row['328'] == 1 else 'N'
                diagnose.professor_329 = 'S' if row['329'] == 1 else 'N'
                diagnose.professor_330 = 'S' if row['330'] == 1 else 'N'
                diagnose.professor_331 = 'S' if row['331'] == 1 else 'N'
                diagnose.professor_333 = 'S' if row['333'] == 1 else 'N'
                diagnose.professor_338 = 'S' if row['338'] == 1 else 'N'
                diagnose.professor_339 = 'S' if row['339'] == 1 else 'N'
                diagnose.professor_341 = 'S' if row['341'] == 1 else 'N'
                diagnose.professor_342 = 'S' if row['342'] == 1 else 'N'
                diagnose.professor_343 = 'S' if row['343'] == 1 else 'N'
                diagnose.professor_344 = 'S' if row['344'] == 1 else 'N'
                diagnose.professor_345 = 'S' if row['345'] == 1 else 'N'
                diagnose.professor_346 = 'S' if row['346'] == 1 else 'N'
                diagnose.professor_347 = 'S' if row['347'] == 1 else 'N'
                diagnose.professor_348 = 'S' if row['348'] == 1 else 'N'
                diagnose.professor_350 = 'S' if row['350'] == 1 else 'N'
                diagnose.professor_351 = 'S' if row['351'] == 1 else 'N'
                diagnose.professor_352 = 'S' if row['352'] == 1 else 'N'
                diagnose.professor_353 = 'S' if row['353'] == 1 else 'N'
                diagnose.professor_354 = 'S' if row['354'] == 1 else 'N'

                # Save the diagnose object to the database
                diagnose.save()

            messages.success(request, "Planilha de Matemática carregada e processada com sucesso!")
            return redirect('habilidades2')

        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")
            return redirect('habilidades2')

    return render(request, 'habilidades2.html')


def habilidades_view(request):
    habilidades = Habilidade.objects.all()
    return render(request, 'habilidades.html', {'habilidades': habilidades})

def habilidades2_view(request):
    habilidades = DiagnoseMatematicaProf.objects.all()
    return render(request, 'habilidades2.html', {'habilidades': habilidades})

def habilidades3_view(request):
    habilidades = DiagnoseAnosFinaisProfPort.objects.all()
    return render(request, 'habilidades2.html', {'habilidades': habilidades})

def habilidades4_view(request):
    habilidades = DiagnoseAnosFinaisProfMat.objects.all()
    return render(request, 'habilidades4.html', {'habilidades': habilidades})

def lingua_matematica_prof_view(request):
    turmas = [
        '300', '301', '302', '305', '306', '308', '310', 
        '317', '318', '319', '320', '323', '324', '328', 
        '329', '330', '331', '333', '338', '339', '341', 
        '342', '343', '344', '345', '346', '347', '348', 
        '350', '351', '352', '353', '354'
    ]

    itens = []
    total_corretas = 0
    total_erradas = 0
    total_respostas = 0

    itens_db = DiagnoseMatematicaProf.objects.all()

    for item in itens_db:
        respostas = {}
        for turma in turmas:
            resposta = getattr(item, f'professor_{turma}', 'N')
            respostas[turma] = resposta
            if resposta == 'S':
                total_corretas += 1
            else:
                total_erradas += 1
            total_respostas += 1
        itens.append({
            'numero': item.item,
            'habilidade': item.habilidade,
            'descricao_habilidade': item.descricao_habilidade,
            'respostas': respostas
        })

    percentual_acertos = (total_corretas / total_respostas) * 100 if total_respostas > 0 else 0
    percentual_erros = (total_erradas / total_respostas) * 100 if total_respostas > 0 else 0

    uploaded_file_url = None

    if request.method == 'POST':
        if 'upload_planilha' in request.POST and request.FILES.get('planilha'):
            planilha = request.FILES['planilha']
            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)

            try:
                df = pd.read_excel(fs.path(filename))

                for index, row in df.iterrows():
                    item_num = row['Item']
                    habilidade = row['Habilidade']

                    diagnose, created = DiagnoseMatematicaProf.objects.get_or_create(
                        item=item_num,
                        habilidade=habilidade
                    )

                    for turma in turmas:
                        resposta = row.get(str(turma), None)
                        resposta = 'S' if resposta == 1 else 'N'

                        setattr(diagnose, f'professor_{turma}', resposta)

                    diagnose.save()

                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {e}")

            return redirect('lingua_matematica_prof_view')

        if 'salvar_respostas' in request.POST:
            for item in itens:
                diagnose = DiagnoseMatematicaProf.objects.get(item=item['numero'])
                for turma in turmas:
                    nova_resposta = request.POST.get(f'respostas_{item["numero"]}_{turma}', 'N')
                    setattr(diagnose, f'professor_{turma}', nova_resposta)
                diagnose.save()

            messages.success(request, "Respostas salvas com sucesso!")
            return redirect('lingua_matematica_prof_view')

    return render(request, 'lingua_matematica_prof.html', {
        'turmas': turmas,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'percentual_acertos': round(percentual_acertos, 2),
        'percentual_erros': round(percentual_erros, 2),
        'uploaded_file_url': uploaded_file_url
    })

def get_diagnose_data_matematica(request):
    turmas = [
        '300', '301', '302', '305', '306', '308', '310', 
        '317', '318', '319', '320', '323', '324', '328', 
        '329', '330', '331', '333', '338', '339', '341', 
        '342', '343', '344', '345', '346', '347', '348', 
        '350', '351', '352', '353', '354'
    ]

    items = []
    for item in DiagnoseMatematicaProf.objects.all():
        responses = {f"professor_{turma}": getattr(item, f"professor_{turma}", "N") for turma in turmas}
        items.append({
            "numero": item.item,
            "habilidade": item.habilidade,
            "descricao_habilidade": item.descricao_habilidade,
            "respostas": responses
        })
    
    return JsonResponse({"items": items, "turmas": turmas})


# =============================================
# Modelos de Portugues professor anos finais
# =============================================
def habilidades3_view(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                diagnose, created = DiagnoseMatematicaProf.objects.get_or_create(
                    item=row['Item'],
                    habilidade=row['Habilidade']
                )

                for turma in ['101', '102', '103', '104', '105', '106', '107', '109', '110', '112', '114', '117', '119', '120', '121', '124', '126', '128', '129', '130', '131', '134', '135', '137', '138', '139', '140', '142', '143', '144', '145', '146', '147', '171']:
                    resposta = row.get(str(turma), '2')  # Considerando que 'Branco' é o valor default
                    setattr(diagnose, f'professor_{turma}', resposta)

                diagnose.save()

            messages.success(request, "Planilha carregada e processada com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")
        return redirect('habilidades3')

    habilidades = DiagnoseMatematicaProf.objects.all()
    return render(request, 'habilidades3.html', {'habilidades': habilidades})


def lingua_portuguesa_prof_finais_view(request):
    turmas = [
        '101', '102', '103', '104', '105', '106', '107', '109', '110', '112', '114', 
        '117', '119', '120', '121', '124', '126', '128', '129', '130', '131', '134', 
        '135', '137', '138', '139', '140', '142', '143', '144', '145', '146', '147', '171'
    ]

    itens = []
    total_corretas = 0
    total_erradas = 0
    total_brancos = 0
    total_respostas = 0  # Variável para armazenar o total de respostas

    # Busca todos os itens no banco de dados
    itens_db = DiagnoseAnosFinaisProfPort.objects.all()

    for item in itens_db:
        respostas = {}
        for turma in turmas:
            # Limpa e normaliza a resposta (remove espaços extras e converte para minúsculas)
            resposta = getattr(item, f'professor_{turma}', 'Branco').strip().lower()
            respostas[turma] = resposta  # Mantém o valor limpo do banco de dados

            if resposta == '1':  # Acerto
                total_corretas += 1
            elif resposta == '0':  # Erro
                total_erradas += 1
            elif resposta == '2':  # Branco
                total_brancos += 1

            total_respostas += 1  # Incrementa o total de respostas

        itens.append({
            'numero': item.item,
            'habilidade': item.habilidade,
            'descricao_habilidade': item.descricao_habilidade,
            'respostas': respostas
        })

    # Cálculo dos percentuais
    percentual_acertos = (total_corretas / total_respostas) * 100 if total_respostas > 0 else 0
    percentual_erros = (total_erradas / total_respostas) * 100 if total_respostas > 0 else 0
    percentual_brancos = (total_brancos / total_respostas) * 100 if total_respostas > 0 else 0

    # Debug para verificar as contagens de respostas
    print(f"Total Acertos: {total_corretas}, Total Erros: {total_erradas}, Total Brancos: {total_brancos}, Total Respostas: {total_respostas}")

    uploaded_file_url = None

    if request.method == 'POST':
        if 'upload_planilha' in request.POST and request.FILES.get('planilha'):
            planilha = request.FILES['planilha']
            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)

            try:
                df = pd.read_excel(fs.path(filename))

                for index, row in df.iterrows():
                    item_num = row['Item']
                    habilidade = row['Habilidade']

                    diagnose, created = DiagnoseAnosFinaisProfPort.objects.get_or_create(
                        item=item_num,
                        habilidade=habilidade
                    )

                    for turma in turmas:
                        resposta = row.get(str(turma), 'Branco')
                        setattr(diagnose, f'professor_{turma}', resposta)

                    diagnose.save()

                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {e}")

            return redirect('lingua_portuguesa_prof_finais_view')

        if 'salvar_respostas' in request.POST:
            for item in itens:
                diagnose = DiagnoseAnosFinaisProfPort.objects.get(item=item['numero'])
                for turma in turmas:
                    nova_resposta = request.POST.get(f'respostas_{item["numero"]}_{turma}', 'Branco')
                    setattr(diagnose, f'professor_{turma}', nova_resposta)
                diagnose.save()

            messages.success(request, "Respostas salvas com sucesso!")
            return redirect('lingua_portuguesa_prof_finais_view')

    # Renderizando a página com os novos valores de brancos
    return render(request, 'lingua_portuguesa_prof_finais.html', {
        'turmas': turmas,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'total_brancos': total_brancos,  # Total de brancos
        'percentual_acertos': round(percentual_acertos, 2),
        'percentual_erros': round(percentual_erros, 2),
        'percentual_brancos': round(percentual_brancos, 2),  # Percentual de brancos
        'uploaded_file_url': uploaded_file_url
    })

def get_diagnose_data_portugues_finais(request):
    turmas = ['101', '102', '103', '104', '105', '106', '107', '109', '110', '112', 
              '114', '117', '119', '120', '121', '124', '126', '128', '129', '130', 
              '131', '134', '135', '137', '138', '139', '140', '142', '143', '144', 
              '145', '146', '147', '171']

    items = []
    for item in DiagnoseAnosFinaisProfPort.objects.all():
        responses = {f"professor_{turma}": getattr(item, f"professor_{turma}", "Branco") for turma in turmas}
        items.append({
            "numero": item.item,
            "habilidade": item.habilidade,
            "descricao_habilidade": item.descricao_habilidade,
            "respostas": responses
        })
    
    return JsonResponse({"items": items, "turmas": turmas})


# =============================================
# Modelos de Matemática professor anos finais
# =============================================
def habilidades4_view(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            # Lê o arquivo Excel usando Pandas
            df = pd.read_excel(file_path)

            # Itera sobre cada linha do dataframe
            for index, row in df.iterrows():
                diagnose, created = DiagnoseAnosFinaisProfMat.objects.get_or_create(
                    item=row['Item'],
                    habilidade=row['Habilidade']
                )

                # Lista de turmas de acordo com o layout de Matemática
                turmas = [
                    '200', '201', '202', '203', '205', '206', '207', '208', '209', '210',
                    '211', '212', '213', '215', '216', '217', '218', '220', '222', '224',
                    '226', '227', '229', '231', '232', '233', '234', '235', '236', '238',
                    '240', '241', '243'
                ]

                # Para cada turma, define o valor da resposta (apenas 0 ou 1)
                for turma in turmas:
                    resposta = row.get(str(turma), 0)  # Default to 0
                    setattr(diagnose, f'professor_{turma}', resposta)

                diagnose.save()  # Salva o objeto no banco de dados

            # Mensagem de sucesso
            messages.success(request, "Planilha carregada e processada com sucesso!")
        except Exception as e:
            # Mensagem de erro
            messages.error(request, f"Erro ao processar o arquivo: {e}")
        return redirect('habilidades4')  # Redireciona para a página de habilidades 4

    # Exibe os dados existentes
    habilidades = DiagnoseAnosFinaisProfMat.objects.all()
    return render(request, 'habilidades4.html', {'habilidades': habilidades})




def matematica_prof_finais_view(request):
    turmas = [
        '200', '201', '202', '203', '205', '206', '207', '208', '209', '210',
        '211', '212', '213', '215', '216', '217', '218', '220', '222', '224', 
        '226', '227', '229', '231', '232', '233', '234', '235', '236', '238', 
        '240', '241', '243'
    ]

    itens = []
    total_corretas = 0
    total_erradas = 0
    total_respostas = 0  # Variável para armazenar o total de respostas

    itens_db = DiagnoseAnosFinaisProfMat.objects.all()

    for item in itens_db:
        respostas = {}
        for turma in turmas:
            resposta = getattr(item, f'professor_{turma}', 'N')  # Default to 'N' (Não)
            respostas[turma] = resposta

            if resposta == 'S':  # Acerto
                total_corretas += 1
            elif resposta == 'N':  # Erro
                total_erradas += 1

            total_respostas += 1  # Incrementa o total de respostas

        itens.append({
            'numero': item.item,
            'habilidade': item.habilidade,
            'descricao_habilidade': item.descricao_habilidade,
            'respostas': respostas
        })

    # Cálculo dos percentuais
    percentual_acertos = (total_corretas / total_respostas) * 100 if total_respostas > 0 else 0
    percentual_erros = (total_erradas / total_respostas) * 100 if total_respostas > 0 else 0

    return render(request, 'lingua_matematica_prof_finais.html', {
        'turmas': turmas,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'percentual_acertos': round(percentual_acertos, 2),
        'percentual_erros': round(percentual_erros, 2)
    })





def get_diagnose_data_matematica_finais(request):
    turmas = ['200', '201', '202', '203', '205', '206', '207', '208', '209', '210',
              '211', '212', '213', '215', '216', '217', '218', '220', '222', '224',
              '226', '227', '229', '231', '232', '233', '234', '235', '236', '238',
              '240', '241', '243']

    items = []
    for item in DiagnoseAnosFinaisProfMat.objects.all():
        responses = {f"professor_{turma}": getattr(item, f"professor_{turma}", "0") for turma in turmas}  # Default to '0'
        items.append({
            "numero": item.item,
            "habilidade": item.habilidade,
            "descricao_habilidade": item.descricao_habilidade,
            "respostas": responses
        })

    return JsonResponse({"items": items, "turmas": turmas})

def habilidades4_view(request):
    turmas = ['200', '201', '202', '203', '205', '206', '207', '208', '209', '210',
              '211', '212', '213', '215', '216', '217', '218', '220', '222', '224',
              '226', '227', '229', '231', '232', '233', '234', '235', '236', '238',
              '240', '241', '243']
    
    habilidades = DiagnoseAnosFinaisProfMat.objects.all()
    
    habilidades_data = []
    for habilidade in habilidades:
        respostas = {turma: getattr(habilidade, f'professor_{turma}', 'N') for turma in turmas}
        habilidades_data.append({
            'item': habilidade.item,
            'habilidade': habilidade.habilidade,
            'descricao_habilidade': habilidade.descricao_habilidade,
            'respostas': respostas
        })
    
    return render(request, 'lingua_matematica_prof_finais.html', {
        'habilidades': habilidades_data,
        'turmas': turmas
    })


def upload_habilidades2(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        # Valida se o arquivo é .xlsx
        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, "Formato de arquivo inválido. Apenas arquivos .xlsx são permitidos.")
            return redirect('habilidades2')

        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            df = pd.read_excel(file_path)
            # Processa o arquivo Excel...
            for index, row in df.iterrows():
                diagnose, created = DiagnoseMatematicaProf.objects.get_or_create(
                    item=row['Item'],
                    habilidade=row['Habilidade']
                )
                # Atualiza as respostas dos professores...
                diagnose.professor_300 = 'S' if row['300'] == 1 else 'N'
                # Continue para os demais campos...
                diagnose.save()

            messages.success(request, "Planilha de Matemática carregada e processada com sucesso!")
            return redirect('habilidades2')

        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")
            return redirect('habilidades2')

    return render(request, 'habilidades2.html')


# views.py
def upload_habilidades4(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        try:
            # Lê o arquivo Excel
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                # Aqui você pode ajustar para o modelo DiagnoseAnosFinaisProfMat ou outro que seja necessário
                diagnose, created = DiagnoseAnosFinaisProfMat.objects.get_or_create(
                    item=row['Item'],
                    habilidade=row['Habilidade']
                )

                # Atualiza os professores (dependendo de como está estruturado o seu modelo)
                # Exemplo: substitua com base nas turmas relevantes para essa função
                diagnose.professor_200 = 'S' if row['200'] == 1 else 'N'
                diagnose.professor_201 = 'S' if row['201'] == 1 else 'N'
                diagnose.professor_202 = 'S' if row['202'] == 1 else 'N'
                diagnose.professor_203 = 'S' if row['203'] == 1 else 'N'
                diagnose.professor_205 = 'S' if row['205'] == 1 else 'N'
                diagnose.professor_206 = 'S' if row['206'] == 1 else 'N'
                diagnose.professor_207 = 'S' if row['207'] == 1 else 'N'
                diagnose.professor_208 = 'S' if row['208'] == 1 else 'N'
                diagnose.professor_209 = 'S' if row['209'] == 1 else 'N'
                diagnose.professor_210 = 'S' if row['210'] == 1 else 'N'
                diagnose.professor_211 = 'S' if row['211'] == 1 else 'N'
                diagnose.professor_212 = 'S' if row['212'] == 1 else 'N'
                diagnose.professor_213 = 'S' if row['213'] == 1 else 'N'
                diagnose.professor_215 = 'S' if row['215'] == 1 else 'N'
                diagnose.professor_216 = 'S' if row['216'] == 1 else 'N'
                diagnose.professor_217 = 'S' if row['217'] == 1 else 'N'
                diagnose.professor_220 = 'S' if row['220'] == 1 else 'N'
                diagnose.professor_222 = 'S' if row['222'] == 1 else 'N'
                diagnose.professor_224 = 'S' if row['224'] == 1 else 'N'
                diagnose.professor_226 = 'S' if row['226'] == 1 else 'N'
                diagnose.professor_227 = 'S' if row['227'] == 1 else 'N'
                diagnose.professor_229 = 'S' if row['229'] == 1 else 'N'
                diagnose.professor_231 = 'S' if row['231'] == 1 else 'N'
                diagnose.professor_232 = 'S' if row['232'] == 1 else 'N'
                diagnose.professor_233 = 'S' if row['233'] == 1 else 'N'
                diagnose.professor_234 = 'S' if row['234'] == 1 else 'N'
                diagnose.professor_235 = 'S' if row['235'] == 1 else 'N'
                diagnose.professor_236 = 'S' if row['236'] == 1 else 'N'
                diagnose.professor_238 = 'S' if row['238'] == 1 else 'N'
                diagnose.professor_240 = 'S' if row['240'] == 1 else 'N'
                diagnose.professor_241 = 'S' if row['241'] == 1 else 'N'
                diagnose.professor_243 = 'S' if row['243'] == 1 else 'N'
                # Continue para os outros campos conforme necessário...

                diagnose.save()

            messages.success(request, "Planilha carregada e processada com sucesso!")
            return redirect('habilidades4')

        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")
            return redirect('habilidades4')

    return render(request, 'habilidades4.html')
###########################################################################################################
from django.shortcuts import render
from .models import Registro, DiagnoseInicProfPort, DiagnoseAnosFinaisProfMat, DiagnoseAnosFinaisProfPort

def dashboard_view(request):
    ano_exame = request.GET.get('ano_exame', '')

    turmas_iniciais = ['401', '403', '404', '406', '408', '409', '410', '413', '414', '415', '417', '421', '423', '426', '428', '429', '430', '431', '432', '433', '434', '435', '436', '437', '438', '439', '441', '442', '447', '451', '471']
    turmas_finais = ['200', '201', '202', '203', '205', '206', '207', '208', '209', '210', '211', '212', '213', '215', '216', '217', '218', '220', '222', '224', '226', '227', '229', '231', '232', '233', '234', '235', '236', '238', '240', '241', '243']
    turmas_portugues_finais = ['101', '102', '103', '104', '105', '106', '107', '109', '110', '112', '114', '117', '119', '120', '121', '124', '126', '128', '129', '130', '131', '134', '135', '137', '138', '139', '140', '142', '143', '144', '145', '146', '147', '171']

    total_acertos_iniciais = total_erros_iniciais = total_branco_iniciais = 0
    total_acertos_finais = total_erros_finais = total_branco_portugues_finais = 0

    # Filtro por ano se aplicável
    filtro_ano = {}
    if ano_exame:
        filtro_ano['ano_exame'] = ano_exame

    for habilidade in DiagnoseInicProfPort.objects.all():
        for turma in turmas_iniciais:
            resposta = getattr(habilidade, f'professor_{turma}', None)
            if resposta == 'S':
                total_acertos_iniciais += 1
            elif resposta == 'N':
                total_erros_iniciais += 1
            elif resposta == 'Branco':
                total_branco_iniciais += 1

    for habilidade in DiagnoseAnosFinaisProfMat.objects.all():
        for turma in turmas_finais:
            resposta = getattr(habilidade, f'professor_{turma}', None)
            if resposta == 'S':
                total_acertos_finais += 1
            elif resposta == 'N':
                total_erros_finais += 1

    for habilidade in DiagnoseAnosFinaisProfPort.objects.all():
        for turma in turmas_portugues_finais:
            resposta = getattr(habilidade, f'professor_{turma}', None)
            if resposta == '1':
                total_acertos_finais += 1
            elif resposta == '0':
                total_erros_finais += 1
            elif resposta == 'Branco':
                total_branco_portugues_finais += 1

    total_respostas_iniciais = total_acertos_iniciais + total_erros_iniciais + total_branco_iniciais
    total_respostas_finais = total_acertos_finais + total_erros_finais + total_branco_portugues_finais

    percentual_acertos_iniciais = (total_acertos_iniciais / total_respostas_iniciais) * 100 if total_respostas_iniciais else 0
    percentual_erros_iniciais = (total_erros_iniciais / total_respostas_iniciais) * 100 if total_respostas_iniciais else 0
    percentual_branco_iniciais = (total_branco_iniciais / total_respostas_iniciais) * 100 if total_respostas_iniciais else 0

    percentual_acertos_finais = (total_acertos_finais / total_respostas_finais) * 100 if total_respostas_finais else 0
    percentual_erros_finais = (total_erros_finais / total_respostas_finais) * 100 if total_respostas_finais else 0
    percentual_branco_portugues_finais = (total_branco_portugues_finais / total_respostas_finais) * 100 if total_respostas_finais else 0

    anos_disponiveis = Registro.objects.values_list('ano_exame', flat=True).distinct().order_by('-ano_exame')

    context = {
        'total_acertos_iniciais': total_acertos_iniciais,
        'total_erros_iniciais': total_erros_iniciais,
        'total_branco_iniciais': total_branco_iniciais,
        'percentual_acertos_iniciais': round(percentual_acertos_iniciais, 2),
        'percentual_erros_iniciais': round(percentual_erros_iniciais, 2),
        'percentual_branco_iniciais': round(percentual_branco_iniciais, 2),

        'total_acertos_finais': total_acertos_finais,
        'total_erros_finais': total_erros_finais,
        'total_branco_portugues_finais': total_branco_portugues_finais,
        'percentual_acertos_finais': round(percentual_acertos_finais, 2),
        'percentual_erros_finais': round(percentual_erros_finais, 2),
        'percentual_branco_portugues_finais': round(percentual_branco_portugues_finais, 2),

        'ano_exame': ano_exame,
        'anos_disponiveis': anos_disponiveis,
    }

    return render(request, 'dashboard.html', context)



################################################################################################################################################
# ##########################################
# # ALUNOS PORTUGUES ANOS INICIAIS
# ##########################################
from django.shortcuts import render
from .models import DiagnoseAlunoPortugues, HabilidadePortugues

def aluno_portugues_view(request):
    # Inicializa variáveis
    series = ['3º', '4º', '5º', '6º']
    serie_3_corretas = serie_4_corretas = serie_5_corretas = serie_6_corretas = 0
    serie_3_erradas = serie_4_erradas = serie_5_erradas = serie_6_erradas = 0
    serie_3_total = serie_4_total = serie_5_total = serie_6_total = 0
    total_corretas = total_erradas = total_respostas = 0
    itens = []

    # Buscar todas as habilidades do banco de dados
    habilidades_dict = {h.habilidade: h.descricao for h in HabilidadePortugues.objects.all()}

    # Buscar dados dos alunos no banco
    itens_db = DiagnoseAlunoPortugues.objects.all()

    for item in itens_db:
        acerto = round(item.acerto, 2)  # Arredondamento para 2 casas decimais
        erro = round(item.erro, 2)  # Arredondamento para 2 casas decimais
        total_corretas += acerto
        total_erradas += erro
        total_respostas += 1

        # Acumula os dados por série
        if item.serie == '3º':
            serie_3_corretas += acerto
            serie_3_erradas += erro
            serie_3_total += 1
        elif item.serie == '4º':
            serie_4_corretas += acerto
            serie_4_erradas += erro
            serie_4_total += 1
        elif item.serie == '5º':
            serie_5_corretas += acerto
            serie_5_erradas += erro
            serie_5_total += 1
        elif item.serie == '6º':
            serie_6_corretas += acerto
            serie_6_erradas += erro
            serie_6_total += 1

        # Criando a lista de itens corretamente
        itens = []
        for item in itens_db:
            acerto = round(item.acerto, 2)  # Arredondamento para 2 casas decimais
            erro = round(item.erro, 2)  # Arredondamento para 2 casas decimais

            # Busca a descrição da habilidade usando o dicionário de habilidades
            descricao = habilidades_dict.get(item.habilidade, "Descrição não encontrada")

            itens.append({
                'serie': item.serie,
                'habilidade': item.habilidade,
                'descricao_habilidade': descricao,  # Agora corretamente associada
                'acerto': acerto,
                'erro': erro
            })

    # Cálculo dos percentuais por série
    serie_3_percentual_acertos = round((serie_3_corretas / serie_3_total) * 100, 2) if serie_3_total > 0 else 0
    serie_3_percentual_erros = round((serie_3_erradas / serie_3_total) * 100, 2) if serie_3_total > 0 else 0
    serie_4_percentual_acertos = round((serie_4_corretas / serie_4_total) * 100, 2) if serie_4_total > 0 else 0
    serie_4_percentual_erros = round((serie_4_erradas / serie_4_total) * 100, 2) if serie_4_total > 0 else 0
    serie_5_percentual_acertos = round((serie_5_corretas / serie_5_total) * 100, 2) if serie_5_total > 0 else 0
    serie_5_percentual_erros = round((serie_5_erradas / serie_5_total) * 100, 2) if serie_5_total > 0 else 0
    serie_6_percentual_acertos = round((serie_6_corretas / serie_6_total) * 100, 2) if serie_6_total > 0 else 0
    serie_6_percentual_erros = round((serie_6_erradas / serie_6_total) * 100, 2) if serie_6_total > 0 else 0

    percentual_acertos = round((total_corretas / total_respostas) * 100, 2) if total_respostas > 0 else 0
    percentual_erros = round((total_erradas / total_respostas) * 100, 2) if total_respostas > 0 else 0

    return render(request, 'lingua_portuguesa_aluno.html', {
        'series': series,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'percentual_acertos': percentual_acertos,
        'percentual_erros': percentual_erros,
        'serie_3_corretas': serie_3_corretas,
        'serie_3_erradas': serie_3_erradas,
        'serie_3_percentual_acertos': serie_3_percentual_acertos,
        'serie_3_percentual_erros': serie_3_percentual_erros,
        'serie_4_corretas': serie_4_corretas,
        'serie_4_erradas': serie_4_erradas,
        'serie_4_percentual_acertos': serie_4_percentual_acertos,
        'serie_4_percentual_erros': serie_4_percentual_erros,
        'serie_5_corretas': serie_5_corretas,
        'serie_5_erradas': serie_5_erradas,
        'serie_5_percentual_acertos': serie_5_percentual_acertos,
        'serie_5_percentual_erros': serie_5_percentual_erros,
        'serie_6_corretas': serie_6_corretas,
        'serie_6_erradas': serie_6_erradas,
        'serie_6_percentual_acertos': serie_6_percentual_acertos,
        'serie_6_percentual_erros': serie_6_percentual_erros
    })



##################################################################################################

def upload_excel_aluno_portugues(request):
    if request.method == "POST" and request.FILES.get("planilha"):
        planilha = request.FILES['planilha']
        fs = FileSystemStorage()
        filename = fs.save(planilha.name, planilha)
        file_path = fs.path(filename)

        # Mapeamento das séries em texto para números
        series_mapping = {
            '3º ano': 3,
            '4º ano': 4,
            '5º ano': 5,
            '6º ano': 6,
            # Adicione mais séries conforme necessário
        }

        try:
            # Verificar se o tipo de arquivo é Excel
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                df = pd.read_excel(file_path, engine='openpyxl')

                # Limpar dados existentes
                DiagnoseAlunoPortugues.objects.all().delete()

                # Processar cada linha da planilha
                for index, row in df.iterrows():
                    try:
                        serie_texto = row.get('AI')  # Supondo que a coluna 'AI' contém a série em texto
                        habilidade = row.get('Habilidade')
                        topico = row.get('Topico')  # Novo campo topico
                        acerto = float(str(row.get('Acerto')).replace(",", ".")) if not pd.isna(row.get('Acerto')) else 0
                        erro = float(str(row.get('Erro')).replace(",", ".")) if not pd.isna(row.get('Erro')) else 0

                        # Converter a série de texto para número
                        serie = series_mapping.get(serie_texto)
                        if serie is None:
                            raise ValueError(f"Série inválida '{serie_texto}' na linha {index + 1}")

                        # Validação dos valores de acerto/erro
                        if not (0 <= acerto <= 1 and 0 <= erro <= 1):
                            raise ValueError(f"Valores inválidos de acerto/erro na linha {index + 1}")

                        # Salvar no banco de dados
                        DiagnoseAlunoPortugues.objects.create(
                            serie=serie,
                            habilidade=habilidade,
                            topico=topico,  # Incluindo o campo topico
                            acerto=acerto,
                            erro=erro
                        )
                    except Exception as e:
                        messages.error(request, f"Erro ao processar a linha {index + 1}: {e}")
                        continue

                messages.success(request, "Planilha carregada e processada com sucesso!")
            else:
                raise ValueError("Formato de arquivo inválido.")

        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")

        return redirect('lingua_portuguesa_aluno_view')

    return render(request, 'upload_page.html')

##################################################################################################

from django.http import JsonResponse
from .models import DiagnoseAlunoPortugues

def get_diagnose_data_inic_alunos_port(request):
    # Lista de séries que serão usadas para os alunos
    series = ['3º', '4º', '5º', '6º']

    # Lista para armazenar os itens e suas respostas associadas
    items = []

    # Recupera todos os itens da tabela DiagnoseAlunoPortugues (ou o modelo equivalente)
    dados_db = DiagnoseAlunoPortugues.objects.all()

    # Itera sobre cada item recuperado do banco de dados
    for item in dados_db:
        # Adiciona os dados de cada item (série, habilidade, acertos e erros) na lista
        items.append({
            "serie": item.serie if item.serie in series else "N/A",  # Verifica se a série está na lista
            "habilidade": item.habilidade if item.habilidade else "N/A",  # Verifica se a habilidade está presente
            "acerto": round(float(item.acerto or 0), 2),  # Formata os acertos e trata valores nulos
            "erro": round(float(item.erro or 0), 2),  # Formata os erros e trata valores nulos
        })

    # Retorna os dados em formato JSON
    return JsonResponse({"items": items, "series": series})


def habilidades_alunos_view(request):
    # Fetch all student data
    alunos = Aluno.objects.all()

    # Fetch all habilidade data
    habilidades = HabilidadePortugues.objects.all()

    return render(request, 'lingua_portuguesa_aluno.html', {
        'alunos': alunos,
        'habilidades': habilidades
    })

##################################################################################################
#SUBIR PLANILHAS COM HABILIDADES DE PORTUGUES E MATEMATICA
##################################################################################################

def upload_habilidades_planilha_view(request):
    if request.method == 'POST':
        planilha = request.FILES.get('planilha')  # Aceitar qualquer arquivo de planilha
        
        if planilha:
            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)

            try:
                # Detectar automaticamente o tipo de planilha e carregar no Pandas
                if filename.endswith('.xlsx') or filename.endswith('.xls'):
                    df = pd.read_excel(fs.path(filename))
                elif filename.endswith('.csv'):
                    df = pd.read_csv(fs.path(filename))
                else:
                    messages.error(request, "Formato de arquivo não suportado. Por favor, envie um arquivo Excel ou CSV.")
                    return redirect('upload_habilidades_planilha_view')

                # Exemplo de processamento de dados genérico (ajustar conforme necessário)
                processar_dados_genericos(df)  # Função genérica para processar a planilha

                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar a planilha: {e}")
            
            return redirect('upload_habilidades_planilha_view')

    return render(request, 'upload_habilidades_planilha.html')

def processar_dados_genericos(df):
    # Exemplo de processamento genérico de planilha
    for index, row in df.iterrows():
        # Faça o processamento genérico dos dados, conforme necessário
        print(row)  # Apenas exibindo cada linha no terminal por enquanto (ajustar com lógica conforme necessário)

def processar_habilidades_matematica(df):
    HabilidadeMatematica.objects.all().delete()  # Limpa dados antigos

    # Certifique-se de que os nomes das colunas estão corretos
    for _, row in df.iterrows():
        serie = row.get('serie', None)
        topico = row.get('topico', None)
        habilidade = row.get('habilidade', None)
        descricao = row.get('descricao', None)

        if serie and topico and habilidade and descricao:
            HabilidadeMatematica.objects.create(
                serie=serie,
                topico=topico,
                habilidade=habilidade,
                descricao=descricao
            )

def processar_habilidades_portugues(df):
    # Limpa os dados antigos antes de inserir os novos
    HabilidadePortugues.objects.all().delete()

    # Certifique-se de que os nomes das colunas estão corretos
    for _, row in df.iterrows():
        serie = row.get('serie', None)
        topico = row.get('topico', None)
        habilidade = row.get('habilidade', None)
        descricao = row.get('descricao', None)

        if serie and topico and habilidade and descricao:
            HabilidadePortugues.objects.create(
                serie=serie,
                topico=topico,
                habilidade=habilidade,
                descricao=descricao
            )

def visualizar_habilidades_matematica(request):
    habilidades = HabilidadeMatematica.objects.all()
    return render(request, 'visualizar_habilidades.html', {'habilidades': habilidades})

def visualizar_habilidades_portugues(request):
    habilidades = HabilidadePortugues.objects.all()  # Busca todas as habilidades de Português no banco
    return render(request, 'habilidades_portugues.html', {'habilidades': habilidades})

def habilidades_matematica_view(request):
    # Lógica para processar e renderizar as habilidades de Matemática
    habilidades = HabilidadeMatematica.objects.all()  # Buscando todos os dados
    return render(request, 'habilidades_matematica.html', {'habilidades': habilidades})

def habilidades_portugues_view(request):
    habilidades = HabilidadePortugues.objects.all()  # Buscando todos os dados
    return render(request, 'habilidades_portugues.html', {'habilidades': habilidades})

from django.shortcuts import render

# View para o upload de habilidades de Matemática
def upload_habilidades_matematica_view(request):
    if request.method == 'POST':
        planilha_matematica = request.FILES.get('planilha_matematica')
        
        if planilha_matematica:
            fs = FileSystemStorage()
            filename_matematica = fs.save(planilha_matematica.name, planilha_matematica)
            uploaded_file_url_matematica = fs.url(filename_matematica)

            try:
                # Processar a planilha de Matemática
                df_matematica = pd.read_excel(fs.path(filename_matematica))
                processar_habilidades_matematica(df_matematica)
                messages.success(request, "Planilha de Matemática carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar a planilha de Matemática: {e}")
            
            return redirect('upload_habilidades_matematica_view')

    return render(request, 'upload_habilidades_matematica.html')

# View para o upload de habilidades de Português
def upload_habilidades_portugues_view(request):
    if request.method == 'POST':
        planilha_portugues = request.FILES.get('planilha_portugues')
        
        if planilha_portugues:
            fs = FileSystemStorage()
            filename_portugues = fs.save(planilha_portugues.name, planilha_portugues)
            uploaded_file_url_portugues = fs.url(filename_portugues)

            try:
                # Processar a planilha de Português
                df_portugues = pd.read_excel(fs.path(filename_portugues))
                processar_habilidades_portugues(df_portugues)  # Processamento da planilha
                messages.success(request, "Planilha de Português carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar a planilha de Português: {e}")
            
            return redirect('upload_habilidades_portugues_view')

    return render(request, 'upload_habilidades_portugues.html')
###############################################################################################################
# ##########################################
# # ALUNOS MATEMÁTICA ANOS INICIAIS
# ##########################################
def aluno_matematica_view(request):
    # Inicialização das variáveis
    series = ['3º', '4º', '5º', '6º']
    serie_3_corretas = serie_4_corretas = serie_5_corretas = serie_6_corretas = 0
    serie_3_erradas = serie_4_erradas = serie_5_erradas = serie_6_erradas = 0
    serie_3_total = serie_4_total = serie_5_total = serie_6_total = 0
    total_corretas = total_erradas = total_respostas = 0
    itens = []

    # Buscar dados do banco
    itens_db = DiagnoseAlunoMatematica.objects.all()

    for item in itens_db:
        try:
            # Convertendo para float se for uma string antes de arredondar
            acerto = round(float(item.acerto), 2)  # Arredondamento para duas casas decimais
            erro = round(float(item.erro), 2)  # Arredondamento para duas casas decimais
        except ValueError:
            # Se não for possível converter, ignorar a linha ou lidar com o erro conforme necessário
            continue

        total_corretas += acerto
        total_erradas += erro
        total_respostas += 1

        # Acumula os dados por série
        if item.serie == '3º':
            serie_3_corretas += acerto
            serie_3_erradas += erro
            serie_3_total += 1
        elif item.serie == '4º':
            serie_4_corretas += acerto
            serie_4_erradas += erro
            serie_4_total += 1
        elif item.serie == '5º':
            serie_5_corretas += acerto
            serie_5_erradas += erro
            serie_5_total += 1
        elif item.serie == '6º':
            serie_6_corretas += acerto
            serie_6_erradas += erro
            serie_6_total += 1

        itens.append({
            'serie': item.serie,
            'habilidade': item.habilidade,
            'acerto': acerto,
            'erro': erro
        })

    # Cálculo dos percentuais por série
    serie_3_percentual_acertos = round((serie_3_corretas / serie_3_total) * 100, 2) if serie_3_total > 0 else 0
    serie_3_percentual_erros = round((serie_3_erradas / serie_3_total) * 100, 2) if serie_3_total > 0 else 0
    serie_4_percentual_acertos = round((serie_4_corretas / serie_4_total) * 100, 2) if serie_4_total > 0 else 0
    serie_4_percentual_erros = round((serie_4_erradas / serie_4_total) * 100, 2) if serie_4_total > 0 else 0
    serie_5_percentual_acertos = round((serie_5_corretas / serie_5_total) * 100, 2) if serie_5_total > 0 else 0
    serie_5_percentual_erros = round((serie_5_erradas / serie_5_total) * 100, 2) if serie_5_total > 0 else 0
    serie_6_percentual_acertos = round((serie_6_corretas / serie_6_total) * 100, 2) if serie_6_total > 0 else 0
    serie_6_percentual_erros = round((serie_6_erradas / serie_6_total) * 100, 2) if serie_6_total > 0 else 0

    percentual_acertos = round((total_corretas / total_respostas) * 100, 2) if total_respostas > 0 else 0
    percentual_erros = round((total_erradas / total_respostas) * 100, 2) if total_respostas > 0 else 0

    uploaded_file_url = None

    if request.method == 'POST':
        if 'upload_planilha' in request.POST and request.FILES.get('planilha'):
            planilha = request.FILES['planilha']

            fs = FileSystemStorage()
            filename = fs.save(planilha.name, planilha)
            uploaded_file_url = fs.url(filename)

            try:
                # Carrega a planilha com pandas
                df = pd.read_excel(fs.path(filename))

                # Limpa a tabela antes de adicionar novos dados
                DiagnoseAlunoMatematica.objects.all().delete()

                # Itera sobre as linhas da planilha e processa cada uma
                for index, row in df.iterrows():
                    try:
                        serie = row['AI']
                        habilidade = row['Habilidade']
                        acerto = float(str(row['Acerto']).replace(",", "."))
                        erro = float(str(row['Erro']).replace(",", "."))

                        # Validação dos dados antes de salvar
                        if not (0 <= acerto <= 1 and 0 <= erro <= 1):
                            raise ValueError(f"Valores inválidos de acerto/erro na linha {index + 1}")

                        DiagnoseAlunoMatematica.objects.create(
                            serie=serie,
                            habilidade=habilidade,
                            acerto=acerto,
                            erro=erro
                        )
                    except Exception as e:
                        messages.error(request, f"Erro ao processar a linha {index + 1}: {e}")

                messages.success(request, "Planilha carregada e processada com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao processar o arquivo: {e}")

            return redirect('aluno_matematica_view')

    return render(request, 'lingua_matematica_aluno.html', {
        'series': series,
        'itens': itens,
        'total_corretas': total_corretas,
        'total_erradas': total_erradas,
        'percentual_acertos': percentual_acertos,
        'percentual_erros': percentual_erros,
        'serie_3_corretas': serie_3_corretas,
        'serie_3_erradas': serie_3_erradas,
        'serie_3_percentual_acertos': serie_3_percentual_acertos,
        'serie_3_percentual_erros': serie_3_percentual_erros,
        'serie_4_corretas': serie_4_corretas,
        'serie_4_erradas': serie_4_erradas,
        'serie_4_percentual_acertos': serie_4_percentual_acertos,
        'serie_4_percentual_erros': serie_4_percentual_erros,
        'serie_5_corretas': serie_5_corretas,
        'serie_5_erradas': serie_5_erradas,
        'serie_5_percentual_acertos': serie_5_percentual_acertos,
        'serie_5_percentual_erros': serie_5_percentual_erros,
        'serie_6_corretas': serie_6_corretas,
        'serie_6_erradas': serie_6_erradas,
        'serie_6_percentual_acertos': serie_6_percentual_acertos,
        'serie_6_percentual_erros': serie_6_percentual_erros,
        'uploaded_file_url': uploaded_file_url
    })


################################################################################################################
def upload_excel_aluno_matematica(request):
    if request.method == "POST" and request.FILES.get("planilha"):
        planilha = request.FILES['planilha']
        fs = FileSystemStorage()
        filename = fs.save(planilha.name, planilha)
        file_path = fs.path(filename)

        # Mapeamento das séries em texto para números
        series_mapping = {
            '3º ano': 3,
            '4º ano': 4,
            '5º ano': 5,
            '6º ano': 6,
            # Adicione mais séries conforme necessário
        }

        try:
            # Verificar se o tipo de arquivo é Excel
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                df = pd.read_excel(file_path, engine='openpyxl')

                # Limpar dados existentes
                DiagnoseAlunoMatematica.objects.all().delete()

                # Processar cada linha da planilha
                for index, row in df.iterrows():
                    try:
                        # Ajuste os nomes das colunas com os corretos
                        serie_texto = row.get('AI')  # Supondo que a coluna 'AI' contém a série em texto
                        habilidade = row.get('Habilidade')
                        acerto = float(str(row.get('Acerto')).replace(",", ".")) if not pd.isna(row.get('Acerto')) else 0
                        erro = float(str(row.get('Erro')).replace(",", ".")) if not pd.isna(row.get('Erro')) else 0

                        # Converter a série de texto para número
                        serie = series_mapping.get(serie_texto)
                        if serie is None:
                            raise ValueError(f"Série inválida '{serie_texto}' na linha {index + 1}")

                        # Validação dos valores de acerto/erro
                        if not (0 <= acerto <= 1 and 0 <= erro <= 1):
                            raise ValueError(f"Valores inválidos de acerto/erro na linha {index + 1}")

                        # Salvar no banco de dados
                        DiagnoseAlunoMatematica.objects.create(
                            serie=serie,  # Salvar a série convertida
                            habilidade=habilidade,
                            acerto=acerto,
                            erro=erro
                        )
                    except Exception as e:
                        messages.error(request, f"Erro ao processar a linha {index + 1}: {e}")
                        continue

                messages.success(request, "Planilha carregada e processada com sucesso!")
            else:
                raise ValueError("Formato de arquivo inválido.")

        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {e}")

        return redirect('aluno_matematica_view')

    return render(request, 'upload_page_matematica.html')

################################################################################################################
def get_diagnose_data_inic_alunos_matematica(request):
    # Lista de séries que serão usadas para os alunos
    series = ['3º', '4º', '5º', '6º']

    # Lista para armazenar os itens e suas respostas associadas
    items = []

    # Recupera todos os itens da tabela DiagnoseAlunoMatematica
    dados_db = DiagnoseAlunoMatematica.objects.all()

    # Itera sobre cada item recuperado do banco de dados
    for item in dados_db:
        # Adiciona os dados de cada item (série, habilidade, acertos e erros) na lista
        items.append({
            "serie": item.serie,  # Série do aluno
            "habilidade": item.habilidade,  # Habilidade correspondente
            "acerto": item.acerto,  # Total de acertos
            "erro": item.erro  # Total de erros
        })

    # Retorna os dados em formato JSON
    return JsonResponse({"items": items, "series": series})
################################################################################################################

def matematica_aluno_view(request):
    # Lógica da view
    return render(request, 'lingua_matematica_aluno.html')
################################################################################################################

def habilidades_view(request):
    habilidades_matematica = HabilidadeMatematica.objects.all()
    habilidades_portugues = HabilidadePortugues.objects.all()

    return render(request, 'habilidades.html', {
        'habilidades_matematica': habilidades_matematica,
        'habilidades_portugues': habilidades_portugues
    })
#################################################################################################################
from django.db.models import Avg

def search_view(request):
    habilidade = request.GET.get('habilidade', '')
    disciplina_portugues = request.GET.get('disciplina_portugues')
    disciplina_matematica = request.GET.get('disciplina_matematica')
    tipo_usuario_professor = request.GET.get('tipo_usuario_professor')
    tipo_usuario_aluno = request.GET.get('tipo_usuario_aluno')
    ano_inicial = request.GET.get('ano_inicial')
    ano_final = request.GET.get('ano_final')

    # Buscando habilidades e diagnósticos
    habilidades_portugues = HabilidadePortugues.objects.all()
    habilidades_matematica = HabilidadeMatematica.objects.all()
    diagnostico_portugues = DiagnoseAlunoPortugues.objects.all()
    diagnostico_matematica = DiagnoseAlunoMatematica.objects.all()

    # Filtrando por habilidade nas tabelas de habilidades e diagnósticos
    if habilidade:
        habilidades_portugues = habilidades_portugues.filter(habilidade__icontains=habilidade)
        habilidades_matematica = habilidades_matematica.filter(habilidade__icontains=habilidade)
        diagnostico_portugues = diagnostico_portugues.filter(habilidade__icontains=habilidade)
        diagnostico_matematica = diagnostico_matematica.filter(habilidade__icontains=habilidade)

    # Filtros por disciplina
    if disciplina_portugues:
        habilidades_matematica = HabilidadeMatematica.objects.none()  # Esconde Matemática se Português for selecionado
    if disciplina_matematica:
        habilidades_portugues = HabilidadePortugues.objects.none()  # Esconde Português se Matemática for selecionado

    # Filtro por Anos Iniciais e Anos Finais
    if ano_inicial:
        habilidades_portugues = habilidades_portugues.filter(serie__lte=5)
        habilidades_matematica = habilidades_matematica.filter(serie__lte=5)
    if ano_final:
        habilidades_portugues = habilidades_portugues.filter(serie__gt=5)
        habilidades_matematica = habilidades_matematica.filter(serie__gt=5)

    # Garantindo que existam dados para os diagnósticos antes de calcular as médias
    media_acertos_portugues = diagnostico_portugues.aggregate(media_acertos=Avg('acerto'))['media_acertos'] or 0
    media_erros_portugues = diagnostico_portugues.aggregate(media_erros=Avg('erro'))['media_erros'] or 0

    media_acertos_matematica = diagnostico_matematica.aggregate(media_acertos=Avg('acerto'))['media_acertos'] or 0
    media_erros_matematica = diagnostico_matematica.aggregate(media_erros=Avg('erro'))['media_erros'] or 0

    # Preparando os dados para gráficos
    data_alunos = {
        'acertos': [media_acertos_portugues],
        'erros': [media_erros_portugues],
    }

    data_professores = {
        'acertos': [media_acertos_matematica],
        'erros': [media_erros_matematica],
    }

    # Definindo rótulos dinâmicos para os gráficos
    chart_label = "Desempenho"
    if disciplina_portugues:
        chart_label = "Português"
    elif disciplina_matematica:
        chart_label = "Matemática"

    context = {
        'data_alunos': data_alunos,
        'data_professores': data_professores,
        'habilidades_portugues': habilidades_portugues,
        'habilidades_matematica': habilidades_matematica,
        'chart_label': chart_label,
        'tipo_usuario_professor': tipo_usuario_professor,
        'tipo_usuario_aluno': tipo_usuario_aluno,
    }

    return render(request, 'search.html', context)
#################################################################################################################

def home_view(request):
    return render(request, 'base.html')
#################################################################################################################

def ajuda(request):
    # Renderiza a página de ajuda e suporte
    return render(request, 'ajuda.html')
#################################################################################################################

def solicitar_suporte(request):
    # Processa o formulário de solicitação de suporte
    if request.method == 'POST':
        form = SuporteForm(request.POST)
        if form.is_valid():
            form.save()  # Salva a solicitação no banco de dados
            messages.success(request, 'Sua solicitação de suporte foi enviada com sucesso.')
            return redirect('ajuda')
    else:
        form = SuporteForm()
    return render(request, 'ajuda.html', {'form': form})
#################################################################################################################

def feedback_suporte(request):
    # Processa o formulário de feedback de suporte
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o feedback no banco de dados
            messages.success(request, 'Obrigado pelo seu feedback!')
            return redirect('ajuda')
    else:
        form = FeedbackForm()
    return render(request, 'ajuda.html', {'form': form})
#################################################################################################################

def ajuda_view(request):
    return render(request, 'ajuda.html')
#################################################################################################################
@login_required
def seguranca_view(request):
    return render(request, 'seguranca.html')
#################################################################################################################

@login_required
def alterar_senha_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantém o usuário logado após a alteração
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('seguranca_view')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha.html', {'form': form})
#################################################################################################################

@login_required
def configurar_notificacoes_view(request):
    if request.method == 'POST':
        # Aqui você deve capturar as configurações enviadas e salvar as preferências do usuário.
        messages.success(request, 'Configurações de notificação atualizadas com sucesso.')
        return redirect('seguranca_view')  # Redireciona para a página de segurança após salvar as configurações
    return render(request, 'configurar_notificacoes.html')
#################################################################################################################

def upload_exame_view(request):
    if request.method == "POST":
        arquivo_csv = request.FILES.get("arquivo_csv")
        if not arquivo_csv:
            return render(request, "upload_exame.html", {"mensagem": "Nenhum arquivo enviado!"})

        # Caminho completo para salvar o arquivo
        caminho_csv = os.path.join(settings.MEDIA_ROOT, arquivo_csv.name)

        # Salva o arquivo no sistema
        with open(caminho_csv, "wb+") as destino:
            for chunk in arquivo_csv.chunks():
                destino.write(chunk)

        # Processa o CSV e salva no banco de dados
        try:
            processar_csv_e_salvar_no_banco(caminho_csv)
            mensagem = "Upload e processamento concluídos com sucesso!"
        except Exception as e:
            mensagem = f"Ocorreu um erro ao processar o arquivo: {e}"

        return render(request, "upload_exame.html", {"mensagem": mensagem})

    return render(request, "upload_exame.html")
#################################################################################################################

from django.db.models import Q

def gestao_arquivos_view(request):
    ano = request.GET.get('ano_exame', '')
    status = request.GET.get('status', '')
    busca_nome = request.GET.get('busca_nome', '')

    registros = Registro.objects.all()

    if ano:
        registros = registros.filter(ano_exame=ano)
    if status:
        registros = registros.filter(status=status)
    if busca_nome:
        registros = registros.filter(nome__icontains=busca_nome)

    total_registros = registros.count()
    concluintes = registros.filter(status='concluinte').count()
    aprovados = registros.filter(status='aprovado').count()
    reprovados = registros.filter(status='reprovado').count()

    anos_disponiveis = Registro.objects.values_list('ano_exame', flat=True).distinct().order_by('-ano_exame')

    contexto = {
        'total_registros': total_registros,
        'concluintes': concluintes,
        'nao_concluintes': total_registros - concluintes,
        'aprovados': aprovados,
        'reprovados': reprovados,
        'registros': registros,
        'anos_disponiveis': anos_disponiveis,
        'ano_exame': ano,
        'status': status,
        'busca_nome': busca_nome,  # para preencher o campo no template
    }

    return render(request, 'gestao_arquivos.html', contexto)

#################################################################################################################

def relatorios_eja_view(request):
    # Exemplo de dados para exibir no relatório
    context = {
        'titulo': 'Relatórios EJA',
        'descricao': 'Relatórios de desempenho e análises do EJA.',
    }
    return render(request, 'webapp/relatorios_eja.html', context)
#################################################################################################################

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseBadRequest
import re
from .models import Registro

def editar_registro_view(request, id):
    registro = get_object_or_404(Registro, id=id)
    sucesso = False  # Flag para exibir modal de sucesso

    if request.method == 'POST':
        try:
            # Validação do CPF
            cpf = request.POST.get('cpf', registro.cpf).strip()
            if not re.match(r'^\d{11}$', cpf):
                return HttpResponseBadRequest("CPF inválido")

            # Atualizar campos básicos
            registro.ano_exame = request.POST.get('ano_exame', registro.ano_exame)
            registro.nome = request.POST.get('nome', registro.nome)
            registro.cpf = cpf
            registro.observacao = request.POST.get('observacao', registro.observacao)

            # Notas com conversão segura
            def parse_float(value, default=0):
                try:
                    return float(value)
                except (TypeError, ValueError):
                    return default

            registro.portugues = parse_float(request.POST.get('portugues'))
            registro.redacao = parse_float(request.POST.get('redacao'))
            registro.media_ling = (registro.portugues + registro.redacao) / 2
            registro.ingles = parse_float(request.POST.get('ingles'))
            registro.arte = parse_float(request.POST.get('arte'))
            registro.ed_fisica = parse_float(request.POST.get('ed_fisica'))
            registro.historia = parse_float(request.POST.get('historia'))
            registro.geografia = parse_float(request.POST.get('geografia'))
            registro.matematica = parse_float(request.POST.get('matematica'))
            registro.ciencias = parse_float(request.POST.get('ciencias'))

            # Lógica de aprovação
            disciplinas = {
                "Média Linguagem": registro.media_ling,
                "Inglês": registro.ingles,
                "Arte": registro.arte,
                "Educação Física": registro.ed_fisica,
                "História": registro.historia,
                "Geografia": registro.geografia,
                "Matemática": registro.matematica,
                "Ciências": registro.ciencias,
            }

            materias_aprovadas = [m for m, nota in disciplinas.items() if nota >= 7]
            reprovadas = len(disciplinas) - len(materias_aprovadas)

            if reprovadas == 0:
                registro.status = "concluinte"
            elif reprovadas == len(disciplinas):
                registro.status = "reprovado"
            else:
                registro.status = "aprovado"

            registro.save()
            sucesso = True

        except Exception as e:
            messages.error(request, f"Erro ao atualizar o registro: {e}")

    return render(request, 'webapp/editar_registro.html', {
        'registro': registro,
        'sucesso': sucesso
    })


#################################################################################################################

def excluir_registro_view(request, id):
    registro = get_object_or_404(Registro, id=id)
    registro.delete()
    messages.success(request, 'Registro excluído com sucesso.')
    return redirect('gestao_arquivos')  # Redireciona para a página de gestão de arquivos
#################################################################################################################

def processar_planilha(file_path):
    # Leia a planilha
    df = pd.read_excel(file_path)
    
    # Itere sobre as linhas e salve os registros
    for _, row in df.iterrows():
        Registro.objects.create(
            ano_exame=row.get('ANO DO EXAME DE SUPLENCIA', None),
            numero=row.get('NÚMERO', None),
            nome=row.get('NOME', None),
            cpf=row.get('CPF', None),
            portugues=row.get('PORTUGUÊS', None),
            redacao=row.get('REDAÇÃO', None),
            media_ling=row.get('MÉDIA LING', None),
            ingles=row.get('INGLÊS', None),
            arte=row.get('ARTE', None),
            ed_fisica=row.get('ED. FÍSICA', None),
            historia=row.get('HISTÓRIA', None),
            geografia=row.get('GEOGRAFIA', None),
            matematica=row.get('MATEMÁTICA', None),
            ciencias=row.get('CIÊNCIAS', None),
            observacao=row.get('OBSERVAÇÃO', None),
            status=row.get('STATUS', None),
            materias_aprovadas=row.get('MATERIAS APROVADAS', None)
        )
#################################################################################################################

def processar_csv_e_salvar_no_banco(caminho_csv):
    with open(caminho_csv, mode='r', encoding='utf-8') as arquivo_csv:
        leitor = csv.DictReader(arquivo_csv, delimiter=';')
        
        for row in leitor:
            try:
                # Função para converter valores numéricos com vírgula para ponto
                def converter_valor(valor):
                    return float(valor.replace(',', '.')) if valor else 0.0

                # Calculando a média de Linguagem
                portugues = converter_valor(row.get("PORTUGUÊS", "0"))
                redacao = converter_valor(row.get("REDAÇÃO", "0"))
                media_ling = round((portugues + redacao) / 2, 1)  # Média de Português e Redação

                # Lista de disciplinas com suas notas (incluindo a média de Linguagem no lugar de Português e Redação separadas)
                disciplinas = {
                    "Média Linguagem": media_ling,
                    "INGLÊS": converter_valor(row.get("INGLÊS", "0")),
                    "ARTE": converter_valor(row.get("ARTE", "0")),
                    "ED. FÍSICA": converter_valor(row.get("ED. FÍSICA", "0")),
                    "HISTÓRIA": converter_valor(row.get("HISTÓRIA", "0")),
                    "GEOGRAFIA": converter_valor(row.get("GEOGRAFIA", "0")),
                    "MATEMÁTICA": converter_valor(row.get("MATEMÁTICA", "0")),
                    "CIÊNCIAS": converter_valor(row.get("CIÊNCIAS", "0")),
                }

                # Determinando o status
                materias_aprovadas = [materia for materia, nota in disciplinas.items() if nota >= 7]
                total_disciplinas = len(disciplinas)
                disciplinas_reprovadas = total_disciplinas - len(materias_aprovadas)

                if disciplinas_reprovadas == 0:
                    status = "concluinte"
                elif disciplinas_reprovadas == total_disciplinas:
                    status = "reprovado"
                else:
                    status = "aprovado"

                # Criando o registro no banco de dados
                Registro.objects.create(
                    ano_exame=int(row.get("ANO DO EXAME DE SUPLENCIA", "0").strip()),
                    numero=int(row.get("NÚMERO", "0").strip()),
                    nome=row.get("NOME", "").strip(),
                    cpf=row.get("CPF", "").strip(),
                    portugues=portugues,
                    redacao=redacao,
                    media_ling=media_ling,
                    ingles=disciplinas["INGLÊS"],
                    arte=disciplinas["ARTE"],
                    ed_fisica=disciplinas["ED. FÍSICA"],
                    historia=disciplinas["HISTÓRIA"],
                    geografia=disciplinas["GEOGRAFIA"],
                    matematica=disciplinas["MATEMÁTICA"],
                    ciencias=disciplinas["CIÊNCIAS"],
                    observacao=row.get("OBSERVAÇÃO", "").strip(),
                    status=status,
                    materias_aprovadas=";".join(materias_aprovadas)
                )
            except ValueError as e:
                print(f"Erro ao processar linha {row}: {e}")
            except Exception as e:
                print(f"Erro inesperado ao processar linha {row}: {e}")

#################################################################################################################
def gerar_relatorio_pdf(request):
    status = request.GET.get('status', None)
    

    # Fetch records based on the status
    if status:
        registros = Registro.objects.filter(status=status)
        titulo = f"Relatório de Registros - Status: {status.capitalize()}"
    else:
        registros = Registro.objects.all()
        titulo = "Relatório de Registros - Todos os Status"

    # Prepare data for the table
    data = [
        ["NOME", "PORT", "RED", "MÉDIA", "ING", "ART", "ED. FÍS", "HIS", "GEO", "MAT", "CIÊN", "RESULTADO", "OBSERVAÇÃO"]
    ]
    for registro in registros:
        data.append([
            registro.nome,
            registro.portugues,
            registro.redacao,
            registro.media_ling,
            registro.ingles,
            registro.arte,
            registro.ed_fisica,
            registro.historia,
            registro.geografia,
            registro.matematica,
            registro.ciencias,
            registro.status,
            registro.observacao,
        ])

    # Configure the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_{status or "todos"}.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(letter),
        rightMargin=30, leftMargin=30, topMargin=150, bottomMargin=30
    )

    # Dynamic styling for notes
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]

    # Apply dynamic colors for numeric columns
    for row_idx, row in enumerate(data[1:], start=1):  # Start from 1 to skip the header
        for col_idx in range(1, 11):  # Numeric columns (PORT to CIÊN)
            try:
                if float(row[col_idx]) < 7:
                    table_style.append(('TEXTCOLOR', (col_idx, row_idx), (col_idx, row_idx), colors.red))
                else:
                    table_style.append(('TEXTCOLOR', (col_idx, row_idx), (col_idx, row_idx), colors.darkgreen))
            except ValueError:
                pass  # Skip if the cell is not a number

    tabela = Table(data)
    tabela.setStyle(TableStyle(table_style))

    elementos = [tabela]

    # Build the PDF with header on all pages
    doc.build(elementos, onFirstPage=lambda c, d: cabecalho(c, d, status), onLaterPages=lambda c, d: cabecalho(c, d, status))

    return response
#################################################################################################################

def gerar_relatorio_completo_view(request):
    # Fetch all records from the database
    registros = Registro.objects.all()
    titulo = "Relatório Completo de Registros"

    # Prepare data for the table
    data = [
        ["NOME", "PORT", "RED", "MÉDIA", "ING", "ART", "ED. FÍS", "HIS", "GEO", "MAT", "CIÊN", "RESULTADO", "OBSERVAÇÃO"]
    ]
    for registro in registros:
        data.append([
            registro.nome,
            registro.portugues,
            registro.redacao,
            registro.media_ling,
            registro.ingles,
            registro.arte,
            registro.ed_fisica,
            registro.historia,
            registro.geografia,
            registro.matematica,
            registro.ciencias,
            registro.status,
            registro.observacao,
        ])

    # Configure the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_completo.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(letter),
        rightMargin=30,
        leftMargin=30,
        topMargin=150,
        bottomMargin=30
    )

    # Dynamic styling for notes
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]

    # Apply dynamic colors for numeric columns
    for row_idx, row in enumerate(data[1:], start=1):  # Skip header row
        for col_idx in range(1, 11):  # Numeric columns (PORT to CIÊN)
            try:
                if float(row[col_idx]) < 7:
                    table_style.append(('TEXTCOLOR', (col_idx, row_idx), (col_idx, row_idx), colors.red))
                else:
                    table_style.append(('TEXTCOLOR', (col_idx, row_idx), (col_idx, row_idx), colors.darkgreen))
            except ValueError:
                pass  # Skip non-numeric values

    tabela = Table(data)
    tabela.setStyle(TableStyle(table_style))

    elementos = [tabela]

    # Build the PDF with header on all pages
    doc.build(
        elementos,
        onFirstPage=lambda c, d: cabecalho(c, d, None),  # No specific status for the full report
        onLaterPages=lambda c, d: cabecalho(c, d, None)
    )

    return response
#################################################################################################################

def cabecalho(canvas, doc, status):
    canvas.saveState()

    # Paths to the logo images
    logo_esquerda = os.path.join(settings.BASE_DIR, 'static/assets/dist/img/logoEsquerda.png')
    logo_direita = os.path.join(settings.BASE_DIR, 'static/assets/dist/img/logoDireita.png')

    # Logo dimensions
    logo_width = 90
    logo_height = 90

    # Logo positions
    canvas.drawImage(
        ImageReader(logo_esquerda),
        40,  # Margin from the left
        doc.pagesize[1] - logo_height - 20,  # Positioned at the top
        width=logo_width,
        height=logo_height,
        preserveAspectRatio=True,
    )
    canvas.drawImage(
        ImageReader(logo_direita),
        doc.pagesize[0] - logo_width - 40,  # Margin from the right
        doc.pagesize[1] - logo_height - 20,  # Positioned at the top
        width=logo_width,
        height=logo_height,
        preserveAspectRatio=True,
    )

    # Header text centered between the logos
    canvas.setFont("Helvetica-Bold", 12)
    center_x = doc.pagesize[0] / 2  # Horizontal center
    text_y = doc.pagesize[1] - 40  # Adjusted vertical position
    canvas.drawCentredString(center_x, text_y, "ESTADO DO PARÁ")
    canvas.drawCentredString(center_x, text_y - 15, "PREFEITURA MUNICIPAL DE CANAÃ DOS CARAJÁS")
    canvas.drawCentredString(center_x, text_y - 30, "SECRETARIA MUNICIPAL DE EDUCAÇÃO - SEMED")

    # Add report title below the logos and header text
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(
        center_x,
        text_y - 60,  # Positioned below the header text
        f"Relatório Completo de Registros",
    )

    canvas.restoreState()
#################################################################################################################

def cabecalho(canvas, doc, status):
    canvas.saveState()

    # Verificar e carregar os logos
    logo_esquerda_path = Path(settings.BASE_DIR) / 'static/assets/dist/img/logoEsquerda.png'
    logo_direita_path = Path(settings.BASE_DIR) / 'static/assets/dist/img/logoDireita.png'

    if not logo_esquerda_path.exists() or not logo_direita_path.exists():
        raise FileNotFoundError(f"Os logos não foram encontrados: {logo_esquerda_path}, {logo_direita_path}")

    # Dimensões e posições
    logo_width = 90
    logo_height = 90

    canvas.drawImage(
        str(logo_esquerda_path),
        40,  # Margem à esquerda
        doc.pagesize[1] - logo_height - 20,  # Posição no topo
        width=logo_width,
        height=logo_height,
        preserveAspectRatio=True,
    )
    canvas.drawImage(
        str(logo_direita_path),
        doc.pagesize[0] - logo_width - 40,  # Margem à direita
        doc.pagesize[1] - logo_height - 20,  # Posição no topo
        width=logo_width,
        height=logo_height,
        preserveAspectRatio=True,
    )

    # Texto no cabeçalho
    canvas.setFont("Helvetica-Bold", 12)
    center_x = doc.pagesize[0] / 2  # Centralização horizontal
    text_y = doc.pagesize[1] - 40  # Ajuste vertical
    canvas.drawCentredString(center_x, text_y, "ESTADO DO PARÁ")
    canvas.drawCentredString(center_x, text_y - 15, "PREFEITURA MUNICIPAL DE CANAÃ DOS CARAJÁS")
    canvas.drawCentredString(center_x, text_y - 30, "SECRETARIA MUNICIPAL DE EDUCAÇÃO - SEMED")

    # Título do relatório
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(
        center_x,
        text_y - 60,  # Abaixo do cabeçalho
        f"Relatório de Registros - Status: {status.capitalize() if status else 'Todos'}",
    )

    canvas.restoreState()

#################################################################################################################



def formatar_cpf(cpf):
    """Formata um CPF no formato XXX.XXX.XXX-XX"""
    # Remove caracteres não numéricos
    cpf_numerico = sub(r'\D', '', cpf)
    # Verifica se o CPF tem exatamente 11 dígitos
    if len(cpf_numerico) == 11:
        return f"{cpf_numerico[:3]}.{cpf_numerico[3:6]}.{cpf_numerico[6:9]}-{cpf_numerico[9:]}"
    return cpf  # Retorna o CPF original caso esteja inválido
#################################################################################################################

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from pathlib import Path
from django.conf import settings
import locale
from datetime import datetime

def emitir_certificado_view(request, id):
    registro = get_object_or_404(Registro, id=id)

    # Set the certificate issuance date if not already set
    if not registro.certificado_data_emissao:
        registro.certificado_data_emissao = now().date()
        registro.certificado_emitido = True
        registro.save()

    # Response setup for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{registro.nome}.pdf"'

    # Custom page size for certificate (297mm x 210mm in points, landscape orientation)
    certificado_width = 842  # Width in points (297mm)
    certificado_height = 595  # Height in points (210mm)
    pdf = canvas.Canvas(response, pagesize=(certificado_width, certificado_height))

    # Add certificate background image
    background_image_path = Path(settings.BASE_DIR) / "static/assets/certificadoDeConclusaoFrente.png"
    if not background_image_path.exists():
        return HttpResponse(f"Erro: A imagem de fundo do certificado não foi encontrada no caminho: {background_image_path}")
    
    pdf.drawImage(str(background_image_path), 0, 0, width=certificado_width, height=certificado_height)

    # Set locale for Brazilian Portuguese
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    # Format the date in the desired format
    data_emissao_extenso = registro.certificado_data_emissao.strftime("%d de %B de %Y").title()  # Ex: 05 de dezembro de 2024
    data_emissao_curto = registro.certificado_data_emissao.strftime("%d/%m/%Y")  # Ex: 05/12/2024

    # Format CPF
    cpf_formatado = formatar_cpf(registro.cpf)

    # Add dynamic text fields
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(certificado_width / 2, 288, registro.nome)  # Name of the recipient
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(certificado_width / 1.3, 260, f"{cpf_formatado}")
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(certificado_width / 1.7, 183, f"{data_emissao_extenso}")

    # Save and finalize the PDF
    pdf.showPage()
    # Add back side of the certificate
    back_image_path = Path(settings.BASE_DIR) / "static/assets/certificadoDeConclusaoVerso.png"
    if not back_image_path.exists():
        return HttpResponse(f"Erro: A imagem de fundo do verso não foi encontrada no caminho: {back_image_path}")

    pdf.drawImage(str(back_image_path), 0, 0, width=certificado_width, height=certificado_height)

    # # Add dynamic content for the back page (e.g., scores table)
    # pdf.setFont("Helvetica-Bold", 12)
    # pdf.drawString(50, certificado_height - 100, "Pontuação Obtida nos Exames Realizados:")
    
    # Example data structure for scores (this should come from your database or logic)
    # Prepare data for the table from the database
    scores = [
        ["Linguagens", "Língua Portuguesa", f"{registro.media_ling}", "Edital nº 010, 02/10/2024", "Aprovado(a)"],
        ["Linguagens", "Arte", f"{registro.arte}", "Edital nº 010, 02/10/2024", "Aprovado(a)"],
        ["Linguagens", "Educação Física", f"{registro.ed_fisica}", "Edital nº 010, 02/10/2024", "Aprovado(a)"],
        ["Linguagens", "Língua Inglesa", f"{registro.ingles}", "Edital nº 010, 02/10/2024", "Aprovado(a)"],
        ["Matemática", "Matemática", f"{registro.matematica}", "Edital nº 010, 02/10/2024", "Aprovado(a)"],
        ["Ciências da Natureza", "Ciências", f"{registro.ciencias}", "Edital nº 010, 02/10/2024", "Aprovado(a)"],
        ["Ciências Humanas", "Geografia", f"{registro.geografia}", "Edital nº 010, 02/10/2024", "Aprovado(a)"],
        ["Ciências Humanas", "História", f"{registro.historia}", "Edital nº 010, 02/10/2024", "Aprovado(a)"],
    ]

    table_data = [["Área de Conhecimento", "Componente Curricular", "Pontuação Obtida", "Edital Nº e Data", "Resultado"]] + scores
    table = Table(table_data, colWidths=[120, 150, 100, 150, 100])

    # Apply table styles
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Set the position of the table
    table.wrapOn(pdf, 50, 300)
    table.drawOn(pdf, 110, certificado_height - 450)

    # Add the date of issuance on the back page
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(certificado_width / 1.299, 426, f"{data_emissao_curto}")


    # Save and finalize the PDF
    pdf.showPage()
    pdf.save()

    return response
#################################################################################################################

import locale
from datetime import datetime
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Registro


def formatar_cpf(cpf):
    """Formata o CPF no formato XXX.XXX.XXX-XX"""
    cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"


def emitir_atestado_view(request, id):
    if request.method == 'POST':
        # Capturar dados enviados via POST
        rg = request.POST.get('rg')
        data_nascimento = request.POST.get('dataNascimento')
        cidade_nascimento = request.POST.get('cidadeNascimento')
        nome_pai = request.POST.get('nomePai')
        nome_mae = request.POST.get('nomeMae')

        # Validar campos obrigatórios
        if not all([rg, data_nascimento, cidade_nascimento, nome_pai, nome_mae]):
            return JsonResponse({'error': 'Todos os campos são obrigatórios!'}, status=400)

        # Buscar registro do aluno
        registro = get_object_or_404(Registro, id=id)

        # Atualizar os campos do registro
        registro.rg = rg
        registro.data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
        registro.cidade_nascimento = cidade_nascimento
        registro.nome_pai = nome_pai
        registro.nome_mae = nome_mae

        # Define a data de emissão se não estiver definida
        if not registro.atestado_data_emissao:
            registro.atestado_data_emissao = datetime.now().date()
            registro.atestado_emitido = True
        registro.save()

        # Configuração da resposta do PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="atestado_{registro.nome}.pdf"'

        # Caminho da logo
        logo_image_path = Path(settings.BASE_DIR) / "static/assets/logo.png"
        if not logo_image_path.exists():
            return JsonResponse({'error': 'A imagem da logo não foi encontrada!'}, status=500)

        # Gerar PDF
        pdf = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        # Adicionar a logo mais ao topo
        logo_width = 70  # Largura da logo
        logo_height = 70  # Altura da logo
        logo_x = (width - logo_width) / 2  # Centraliza horizontalmente
        logo_y = height - 100  # Define a posição vertical mais próxima do topo
        pdf.drawImage(str(logo_image_path), logo_x, logo_y, width=logo_width, height=logo_height)


        # Define o locale para português do Brasil
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        except locale.Error:
            # Fallback: usa o locale padrão do sistema
            locale.setlocale(locale.LC_TIME, '')


        # Cabeçalho com separação por linhas
        pdf.setFont("Helvetica-Bold", 10)
        pdf.setFillColor(colors.black)
        pdf.drawCentredString(width / 2, height - 110, "ESTADO DO PARÁ")
        pdf.setFillColor(colors.black)
        pdf.drawCentredString(width / 2, height - 120, "PREFEITURA MUNICIPAL DE CANAÃ DOS CARAJÁS")
        pdf.drawCentredString(width / 2, height - 140, "SECRETARIA MUNICIPAL DE EDUCAÇÃO")
        pdf.drawCentredString(width / 2, height - 130, "NMES PROFª MARIA DIVA RODRIGUES CALDAS (INEP: 15999999)")
        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(width / 2, height - 165, "LEI DE CRIAÇÃO Nº 657/2014 - PMCC/GP")
        pdf.drawCentredString(width / 2, height - 180, "AUTORIZAÇÃO DE ENSINO: 013/2018-CMECC/PA")

        # Linha separadora
        pdf.setLineWidth(1)
        pdf.line(50, height - 185, width - 50, height - 185)

        # Título
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(width / 2, height - 210, "ATESTADO DE CONCLUSÃO")

        # Corpo do texto (justificado)
        pdf.setFont("Helvetica", 12)
        body_text = (
            f"Atestamos para devidos fins de direito que, o aluno(a) {registro.nome}, CPF {formatar_cpf(registro.cpf)}, "
            f"RG {registro.rg if registro.rg else 'Não informado'}, nascido(a) em {registro.data_nascimento.strftime('%d de %B de %Y') if registro.data_nascimento else 'Não informado'}, "
            f"na cidade de {registro.cidade_nascimento if registro.cidade_nascimento else 'Não informada'}, filho(a) da Sra. {registro.nome_mae if registro.nome_mae else 'Não informada'} "
            f"e do Sr. {registro.nome_pai if registro.nome_pai else 'Não informado'}, concluiu neste estabelecimento de ensino o(a) EJA – EXAME DE SUPLÊNCIA – "
            f"ENSINO FUNDAMENTAL, no ano letivo de 2024."
        )
        max_width = 500
        lines = []
        words = body_text.split()
        line = ""

        for word in words:
            test_line = f"{line} {word}".strip()
            if pdf.stringWidth(test_line, "Helvetica", 12) > max_width:
                lines.append(line)
                line = word
            else:
                line = test_line
        lines.append(line)

        y_position = height - 350
        for line in lines:
            pdf.drawString(50, y_position, line)
            y_position -= 20

        # Rodapé
        data_emissao = registro.atestado_data_emissao.strftime("%d de %B de %Y").title()
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(width / 2, 200, f"Canaã dos Carajás/PA, {data_emissao}.")

        # Área de assinatura com linha dupla
        pdf.setLineWidth(1)
        pdf.line(150, 150, width - 150, 150)
        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(width / 2, 130, "Diretor(a) Escolar / Secretário(a) Escolar")

        # Informações de contato com alinhamento central
        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(width / 2, 50, "RUA JOSE DE ANDRADE, 10 – VALE DOURADO – CEP:68537-000 – CANAÃ DOS CARAJÁS – PARÁ")
        pdf.drawCentredString(width / 2, 40, "escola.josededeus@canaadoscarajas.pa.gov.br")

        pdf.showPage()
        pdf.save()

        return response

    return JsonResponse({'error': 'Método não permitido'}, status=405)



#################################################################################################################

# def configurar_certificados_view(request):
#     if request.method == 'POST':
#         # Handle form submission to update configurations
#         pass

#     return render(request, 'configurar_certificados.html', {
#         'settings': current_settings  # Retrieve settings for editing
#     })
#################################################################################################################

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def gerar_pdf_response(request, registro):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="atestado_{registro.nome}.pdf"'

    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Adicionar conteúdo ao PDF
    pdf.drawString(100, height - 100, f"Nome: {registro.nome}")
    pdf.drawString(100, height - 120, f"CPF: {formatar_cpf(registro.cpf)}")
    pdf.drawString(100, height - 140, f"RG: {registro.rg}")
    pdf.drawString(100, height - 160, f"Data de Nascimento: {registro.data_nascimento.strftime('%d/%m/%Y')}")
    pdf.drawString(100, height - 180, f"Cidade de Nascimento: {registro.cidade_nascimento}")
    pdf.drawString(100, height - 200, f"Nome do Pai: {registro.nome_pai}")
    pdf.drawString(100, height - 220, f"Nome da Mãe: {registro.nome_mae}")

    pdf.showPage()
    pdf.save()
    return response
#################################################################################################################


from django.shortcuts import render
from .models import DiagnoseAlunoPortugues

def listar_diagnostico(request):
    alunos = DiagnoseAlunoPortugues.objects.all()

    # Definição das séries
    series = ["3º Ano", "4º Ano", "5º Ano", "6º Ano"]
    estatisticas = {}

    for serie in series:
        alunos_da_serie = alunos.filter(serie=serie)

        if alunos_da_serie.exists():
            total_acertos = sum(aluno.acerto for aluno in alunos_da_serie)
            total_erros = sum(aluno.erro for aluno in alunos_da_serie)
            total = total_acertos + total_erros

            percentual_acertos = (total_acertos / total) * 100 if total > 0 else 0
            percentual_erros = (total_erros / total) * 100 if total > 0 else 0
        else:
            percentual_acertos = 0
            percentual_erros = 0

        estatisticas[serie] = {
            "percentual_acertos": f"{percentual_acertos:.2f}",
            "percentual_erros": f"{percentual_erros:.2f}",
        }

    # Calcular total geral
    total_acertos_geral = sum(aluno.acerto for aluno in alunos)
    total_erros_geral = sum(aluno.erro for aluno in alunos)
    total_geral = total_acertos_geral + total_erros_geral

    percentual_acertos_geral = (total_acertos_geral / total_geral) * 100 if total_geral > 0 else 0
    percentual_erros_geral = (total_erros_geral / total_geral) * 100 if total_geral > 0 else 0

    context = {
        "alunos": alunos,
        "estatisticas": estatisticas,
        "percentual_acertos": f"{percentual_acertos_geral:.2f}",
        "percentual_erros": f"{percentual_erros_geral:.2f}",
    }

    return render(request, 'seu_template.html', context)
################################################################################################################################################

################################################################################################################################################
################################################################################################################################################
######################################################REFATORAÇÃO###############################################################################
################################################################################################################################################

from .models import Disciplina
from django.views.decorators.csrf import csrf_exempt  # Só em testes locais
from django.contrib.auth.hashers import make_password
from .utils import gerar_numero_unico  # Função para número único
from django.http import JsonResponse
from webapp.models import CustomUser  # ou o nome correto do model
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import uuid
from django.http import JsonResponse
from .models import Bairro  # exemplo
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
import weasyprint
from django.contrib.auth import authenticate, login as auth_login
import qrcode
from io import BytesIO
import base64
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Registro
from reportlab.lib.pagesizes import landscape
import locale
from datetime import datetime
from re import sub
import base64
from io import BytesIO
import qrcode
from django.templatetags.static import static


def lista_alunos_eja(request):
    busca = request.GET.get('busca', '')
    ano_exame = request.GET.get('ano_exame', '')
    itens_por_pagina = int(request.GET.get('itens_por_pagina', 25))

    alunos = Registro.objects.all()

    if busca:
        alunos = alunos.filter(
            Q(nome__icontains=busca) |
            Q(cpf__icontains=busca) |
            Q(escola_2024__icontains=busca)
        )

    if ano_exame:
        alunos = alunos.filter(ano_exame=ano_exame)

    # Contar disciplinas com base em substring no campo `disciplinas`
    disciplinas_lista = ['Português', 'Redação', 'Inglês', 'Arte', 'Educação Física', 'História', 'Geografia', 'Matemática', 'Ciências']
    disciplinas_count = {
        d: alunos.filter(disciplinas__icontains=d).count() for d in disciplinas_lista
    }

    paginator = Paginator(alunos.order_by('-id'), itens_por_pagina)
    page_number = request.GET.get('page')
    alunos_paginados = paginator.get_page(page_number)

    qtd_opcoes = [10, 25, 50, 100]
    anos_disponiveis = Registro.objects.values_list('ano_exame', flat=True).distinct().order_by('-ano_exame')

    context = {
        'alunos': alunos_paginados,
        'disciplinas_count': disciplinas_count,
        'qtd_opcoes': qtd_opcoes,
        'anos_disponiveis': anos_disponiveis,
    }
    return render(request, 'webapp/alunos_eja.html', context)
################################################################################################################################################

def index_view(request):
    return render(request, 'index.html')
################################################################################################################################################

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import Disciplina, Registro
import re

def formulario_inscricao(request):
    disciplinas = Disciplina.objects.filter(ativo=True).order_by('nome')

    if request.method == 'POST':
        prova_todas = request.POST.get('prova_todas_disciplinas', '').strip()

        if prova_todas not in ['Sim', 'Não']:
            return HttpResponseBadRequest("Valor inválido para prova_todas_disciplinas.")

        disciplinas_escolhidas = []
        if prova_todas == 'Não':
            disciplinas_escolhidas = request.POST.getlist('disciplinas[]')

            # Verifica se todas as IDs de disciplinas são válidas (números positivos)
            if not all(re.match(r'^\d+$', d) for d in disciplinas_escolhidas):
                return HttpResponseBadRequest("IDs de disciplinas inválidos.")

        # Aqui você pode salvar no banco com segurança, por exemplo:
        # Registro.objects.create(..., disciplinas=",".join(disciplinas_escolhidas), prova_todas_disciplinas=prova_todas)

        return redirect('pagina_de_sucesso')  # ajuste conforme sua URL real

    return render(request, 'formulario_inscricao.html', {
        'disciplinas': disciplinas,
    })

################################################################################################################################################

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db import IntegrityError
from .models import Registro, Disciplina, Bairro
from .utils import gerar_numero_unico  # ajuste se necessário

@csrf_exempt  # Só use assim em desenvolvimento!
def cadastro_usuario_view(request):
    def is_ajax(request):
        # Funciona para JQuery AJAX e fetch com X-Requested-With
        return request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        try:
            nome = request.POST.get('nome_completo')
            email = request.POST.get('email')
            cpf = request.POST.get('cpf_form')
            data_nascimento = request.POST.get('data_nascimento')
            maior_de_18 = request.POST.get('maior_de_18') == 'Sim'

            nome_responsavel = request.POST.get('nome_responsavel')
            cpf_responsavel = request.POST.get('cpf_responsavel')
            rg_responsavel = request.POST.get('rg_responsavel')
            tipo_responsavel = request.POST.get('tipo_responsavel')
            telefone = request.POST.get('telefone')
            telefone_2 = request.POST.get('telefone_2')
            cidade = request.POST.get('cidade')
            endereco = request.POST.get('endereco')

            bairro_id = request.POST.get('bairro')
            bairro_instance = None
            if bairro_id:
                try:
                    bairro_instance = Bairro.objects.get(id=bairro_id)
                except Bairro.DoesNotExist:
                    bairro_instance = None

            fez_exame_supletivo = request.POST.get('fez_exame_supletivo') == 'Sim'
            ano_ultima_prova_raw = request.POST.get('ano_ultima_prova')
            if fez_exame_supletivo:
                if not ano_ultima_prova_raw or not ano_ultima_prova_raw.isdigit():
                    msg = "Você informou que já fez o exame supletivo, mas não preencheu o ano da última prova."
                    if is_ajax(request):
                        return JsonResponse({'status': 'erro', 'msg': msg})
                    messages.error(request, msg)
                    return redirect('cadastro_usuario')
                else:
                    ano_ultima_prova = int(ano_ultima_prova_raw)
            else:
                ano_ultima_prova = None

            prova_todas_disciplinas = request.POST.get('prova_todas_disciplinas')
            if prova_todas_disciplinas == "Sim":
                disciplinas = ", ".join([d.nome for d in Disciplina.objects.filter(ativo=True)])
            else:
                disciplinas = ", ".join(request.POST.getlist('disciplinas[]'))

            possui_necessidade_especial = request.POST.get('possui_necessidade_especial') == 'Sim'
            necessidade_especial_detalhe = request.POST.get('necessidade_especial_detalhe')

            senha_bruta = request.POST.get('senha')
            senha = make_password(senha_bruta)

            local_prova = request.POST.get('local_prova')
            escola_2024 = request.POST.get('escola_2024')
            termos_condicoes = request.POST.get('termos_condicoes') == 'on'

            deseja_participar_aulao = request.POST.get('deseja_participar_aulao', 'Não')
            turno_aulao = request.POST.get('turnos_aulao') if deseja_participar_aulao == 'Sim' else ''

            VALIDOS_TURNOS = ['Matutino', 'Vespertino', 'Noturno']
            if deseja_participar_aulao == 'Sim':
                if not turno_aulao:
                    msg = "Você marcou que deseja participar dos aulões, mas não selecionou o turno desejado."
                    if is_ajax(request):
                        return JsonResponse({'status': 'erro', 'msg': msg})
                    messages.error(request, msg)
                    return redirect('cadastro_usuario')
                elif turno_aulao not in VALIDOS_TURNOS:
                    msg = "Turno de aulão inválido selecionado."
                    if is_ajax(request):
                        return JsonResponse({'status': 'erro', 'msg': msg})
                    messages.error(request, msg)
                    return redirect('cadastro_usuario')

            # Checagem de CPF já cadastrado
            if Registro.objects.filter(cpf=cpf).exists():
                msg = "Já existe um cadastro com este CPF."
                if is_ajax(request):
                    return JsonResponse({'status': 'erro', 'msg': msg})
                messages.error(request, msg)
                return render(request, 'cadastro_usuario.html', {'disciplinas': Disciplina.objects.filter(ativo=True).order_by('nome')})

            ano_exame = 2025
            numero = gerar_numero_unico()

            try:
                novo = Registro.objects.create(
                    nome=nome, email=email, cpf=cpf,
                    data_nascimento=data_nascimento, maior_de_18=maior_de_18,
                    nome_responsavel=nome_responsavel, cpf_responsavel=cpf_responsavel,
                    rg_responsavel=rg_responsavel, tipo_responsavel=tipo_responsavel,
                    telefone=telefone, telefone_2=telefone_2,
                    cidade=cidade, endereco=endereco, bairro=bairro_instance,
                    fez_exame_supletivo=fez_exame_supletivo, ano_ultima_prova=ano_ultima_prova,
                    prova_todas_disciplinas=prova_todas_disciplinas, disciplinas=disciplinas,
                    possui_necessidade_especial=possui_necessidade_especial,
                    necessidade_especial_detalhe=necessidade_especial_detalhe,
                    senha=senha, local_prova=local_prova, escola_2024=escola_2024,
                    termos_condicoes=termos_condicoes, ano_exame=ano_exame, numero=numero,
                    status="Inscrito",
                    portugues=0, redacao=0, media_ling=0, ingles=0, arte=0, ed_fisica=0,
                    historia=0, geografia=0, matematica=0, ciencias=0,
                    deseja_participar_aulao=deseja_participar_aulao, turnos_aulao=turno_aulao,
                )
            except IntegrityError:
                msg = "Erro: Este CPF já foi utilizado em outro cadastro."
                if is_ajax(request):
                    return JsonResponse({'status': 'erro', 'msg': msg})
                messages.error(request, msg)
                return redirect('cadastro_usuario')

            request.session['candidato_id'] = novo.id
            if is_ajax(request):
                return JsonResponse({'status': 'ok', 'redirect_url': '/painel-candidato/'})
            return redirect('painel_candidato')

        except Exception as e:
            msg = f"Erro no cadastro: {str(e)}"
            if is_ajax(request):
                return JsonResponse({'status': 'erro', 'msg': msg})
            messages.error(request, msg)
            return redirect('cadastro_usuario')

    disciplinas = Disciplina.objects.filter(ativo=True).order_by('nome')
    return render(request, 'cadastro_usuario.html', {'disciplinas': disciplinas})





################################################################################################################################################

import re
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Registro
from .utils import gerar_numero_unico  # Função que você deve ter para gerar número único

def reinscricao_usuario(request, cpf):
    # Validação básica do CPF: deve ter exatamente 11 dígitos numéricos
    if not re.match(r'^\d{11}$', cpf):
        return HttpResponseBadRequest("CPF inválido")

    # Busca todos os registros do candidato para 2024
    candidatos = Registro.objects.filter(cpf=cpf, ano_exame=2024).order_by('-id')
    candidato = candidatos.first()
    if not candidato:
        raise Http404("Candidato não encontrado.")

    # Alerta caso haja duplicidade
    if candidatos.count() > 1:
        messages.warning(request, "Atenção: existe mais de uma inscrição com esse CPF para 2024. Mostrando a mais recente.")

    # Disciplinas reprovadas (<7)
    disciplinas_aprovadas = {
        "portugues": candidato.portugues,
        "redacao": candidato.redacao,
        "media_ling": candidato.media_ling,
        "ingles": candidato.ingles,
        "arte": candidato.arte,
        "ed_fisica": candidato.ed_fisica,
        "historia": candidato.historia,
        "geografia": candidato.geografia,
        "matematica": candidato.matematica,
        "ciencias": candidato.ciencias,
    }
    disciplinas_reprovadas = [
        nome.capitalize().replace("_", " ")
        for nome, nota in disciplinas_aprovadas.items()
        if nota is not None and nota < 7.0
    ]

    if request.method == 'POST':
        try:
            # Gera novo número único para a reinscrição
            novo_numero = gerar_numero_unico()

            # Cria o novo registro de reinscrição, copiando todos os campos relevantes
            novo_registro = Registro.objects.create(
                ano_exame=2025,  # Ano da reinscrição
                numero=novo_numero,
                nome=candidato.nome,
                cpf=candidato.cpf,
                portugues=0,
                redacao=0,
                media_ling=0,
                ingles=0,
                arte=0,
                ed_fisica=0,
                historia=0,
                geografia=0,
                matematica=0,
                ciencias=0,
                observacao='',
                status='Inscrito',
                materias_aprovadas='',
                certificado_emitido=False,
                certificado_data_emissao=None,
                certificado_numero='',
                atestado_emitido=False,
                atestado_data_emissao=None,
                atestado_numero='',
                email=candidato.email,
                data_nascimento=candidato.data_nascimento,
                maior_de_18=candidato.maior_de_18,
                nome_responsavel=candidato.nome_responsavel,
                cpf_responsavel=candidato.cpf_responsavel,
                rg_responsavel=candidato.rg_responsavel,
                tipo_responsavel=candidato.tipo_responsavel,
                telefone=candidato.telefone,
                telefone_2=candidato.telefone_2,
                cidade=candidato.cidade,
                endereco=candidato.endereco,
                bairro=candidato.bairro,
                fez_exame_supletivo=candidato.fez_exame_supletivo,
                ano_ultima_prova=None,  # ou 0, conforme sua lógica
                prova_todas_disciplinas=candidato.prova_todas_disciplinas,
                disciplinas=', '.join(disciplinas_reprovadas),  # Só reinscreve nas reprovadas!
                possui_necessidade_especial=candidato.possui_necessidade_especial,
                necessidade_especial_detalhe=candidato.necessidade_especial_detalhe,
                senha=candidato.senha,
                local_prova=candidato.local_prova,
                escola_2024=candidato.escola_2024,
                termos_condicoes=True,
                reinscricao=True,
                reinscrito=False,
                deseja_participar_aulao=candidato.deseja_participar_aulao,
                turnos_aulao=candidato.turnos_aulao,
                # Os campos token e datas podem ser deixados default (None)
            )

            # Marca o registro antigo como reinscrito
            candidato.reinscrito = True
            candidato.save(update_fields=['reinscrito'])

            messages.success(request, "Reinscrição realizada com sucesso!")
            # Opcional: salvar o novo id na sessão para login automático
            request.session['candidato_id'] = novo_registro.id
            return redirect('painel_candidato')  # ajuste se necessário
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao realizar a reinscrição: {e}")

    return render(request, 'webapp/reinscricao_form.html', {
        'candidato': candidato,
        'disciplinas_reprovadas': disciplinas_reprovadas,
    })




################################################################################################################################################

def listar_disciplinas(request):
    disciplinas = Disciplina.objects.filter(ativo=True).values('id', 'nome')
    return JsonResponse(list(disciplinas), safe=False)
################################################################################################################################################

def gerar_numero_unico():
    ultimo = Registro.objects.order_by('-numero').first()
    return ultimo.numero + 1 if ultimo else 1
################################################################################################################################################

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from .models import Registro

@csrf_exempt  # ⚠️ Remova isso se não for necessário para chamadas externas
def verificar_cpf_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'erro', 'mensagem': 'Requisição inválida'}, status=400)

    cpf = request.POST.get('cpf', '').strip()

    # Validação do CPF: exatamente 11 dígitos
    if not re.match(r'^\d{11}$', cpf):
        return JsonResponse({'status': 'erro', 'mensagem': 'CPF inválido'}, status=400)

    if Registro.objects.filter(cpf=cpf).exists():
        return JsonResponse({'status': 'existe'})
    else:
        return JsonResponse({'status': 'nao_existe'})



################################################################################################################################################

from django.http import JsonResponse
import re
from .models import CustomUser

def verificar_cpf(request):
    cpf = request.POST.get('cpf', '').strip()

    # Validação de CPF (exatamente 11 dígitos numéricos)
    if not re.match(r'^\d{11}$', cpf):
        return JsonResponse({'status': 'error', 'message': 'CPF inválido.'}, status=400)

    user = CustomUser.objects.filter(cpf=cpf).first()

    if user:
        if user.is_superuser:
            return JsonResponse({'status': 'success', 'redirect_url': '/admin/'})
        else:
            return JsonResponse({'status': 'error', 'message': 'CPF não é de um administrador.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'CPF não encontrado.'})

################################################################################################################################################

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from .models import CustomUser

@csrf_exempt  # ⚠️ Remover se CSRF estiver sendo usado corretamente no frontend
def verificar_cpf_admin(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Requisição inválida.'}, status=400)

    cpf = request.POST.get('cpf', '').strip()

    # Validação do CPF (11 dígitos numéricos)
    if not re.match(r'^\d{11}$', cpf):
        return JsonResponse({'status': 'error', 'message': 'CPF inválido.'}, status=400)

    user = CustomUser.objects.filter(cpf=cpf).first()

    if user and user.is_superuser:
        return JsonResponse({'status': 'success', 'redirect_url': '/login/'})
    elif user:
        return JsonResponse({'status': 'error', 'message': 'CPF não tem acesso administrativo.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'CPF não encontrado.'})

################################################################################################################################################

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseBadRequest
import re
from .models import Registro

def login_candidato(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf', '').strip()
        senha = request.POST.get('senha', '').strip()

        # Validação básica do CPF
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            messages.error(request, 'CPF inválido. Use o formato 000.000.000-00.')
            return render(request, 'login_candidato.html')

        if not senha:
            messages.error(request, 'Senha não informada.')
            return render(request, 'login_candidato.html')

        # Busca segura
        registros = Registro.objects.filter(cpf=cpf).order_by('-id')

        if not registros.exists():
            messages.error(request, 'CPF não encontrado.')
            return render(request, 'login_candidato.html')

        # Seleciona o mais recente
        candidato = registros.first()

        # Impede login com conta antiga, se houver reinscrição válida
        possui_reinscricao = registros.filter(reinscricao=True).exclude(id=candidato.id).exists()
        if possui_reinscricao and not candidato.reinscricao:
            messages.error(request, 'Utilize a conta mais recente de reinscrição para fazer login.')
            return render(request, 'login_candidato.html')

        # Validação da senha
        if check_password(senha, candidato.senha):
            request.session['candidato_id'] = candidato.id
            return redirect('painel_candidato')
        else:
            messages.error(request, 'Senha incorreta.')

    return render(request, 'login_candidato.html')

################################################################################################################################################

# ... imports iguais

from django.shortcuts import render, redirect, get_object_or_404
from .models import Registro, Disciplina

def painel_candidato(request):
    candidato_id = request.session.get('candidato_id')
    if not candidato_id:
        return redirect('login_candidato')

    candidato_base = get_object_or_404(Registro, id=candidato_id)
    cpf = candidato_base.cpf

    anos_disponiveis = sorted(
        set(int(a) for a in Registro.objects.filter(cpf=cpf).values_list('ano_exame', flat=True)),
        reverse=True
    )

    ano_selecionado = request.GET.get('ano')
    if not ano_selecionado:
        ano_selecionado = str(candidato_base.ano_exame)
    ano_selecionado_int = int(ano_selecionado)

    candidato_qs = Registro.objects.filter(cpf=cpf, ano_exame=ano_selecionado_int).order_by('-id')
    candidato = candidato_qs.first()
    if not candidato:
        return redirect('login_candidato')

    # Apenas para 2024 (ou ano que você desejar)
    mostrar_reinscricao = (
        ano_selecionado_int == 2024 and
        int(getattr(candidato, 'reinscricao', 0)) == 1 and
        int(getattr(candidato, 'reinscrito', 0)) == 0 and
        not Registro.objects.filter(cpf=cpf, ano_exame=2025).exists()
    )

    disciplinas = {
        "Português": candidato.portugues,
        "Matemática": candidato.matematica,
        "Ciências": candidato.ciencias,
        "Arte": candidato.arte,
        "Educação Física": candidato.ed_fisica,
        "História": candidato.historia,
        "Geografia": candidato.geografia,
        "Inglês": candidato.ingles,
    }
    media_aprovacao = 7.0
    disciplinas_aprovadas = {nome: nota for nome, nota in disciplinas.items() if nota is not None and nota >= media_aprovacao}
    disciplinas_pendentes = {nome: nota for nome, nota in disciplinas.items() if nota is None or nota < media_aprovacao}

    disciplinas_lista = []
    if candidato.disciplinas:
        disciplinas_lista = [d.strip() for d in candidato.disciplinas.split(',') if d.strip()]

    total_disciplinas = len(disciplinas_aprovadas) + len(disciplinas_pendentes)
    percentual_aprovadas = round((len(disciplinas_aprovadas) / total_disciplinas) * 100, 1) if total_disciplinas else 0
    percentual_pendentes = round((len(disciplinas_pendentes) / total_disciplinas) * 100, 1) if total_disciplinas else 0

    if len(disciplinas_aprovadas) == len(disciplinas):
        status_final = "Aprovado"
    elif len(disciplinas_aprovadas) > 0:
        status_final = "Parcial"
    else:
        status_final = "Reprovado"

    mostrar_botao_impressao = True

    context = {
        'candidato': candidato,
        'disciplinas_aprovadas': disciplinas_aprovadas,
        'disciplinas_pendentes': disciplinas_pendentes,
        'disciplinas_lista': disciplinas_lista,
        'percentualAprovadas': percentual_aprovadas,
        'percentualPendentes': percentual_pendentes,
        'total_disciplinas': total_disciplinas,
        'todas_disciplinas': Disciplina.objects.filter(ativo=True).order_by('nome'),
        'disciplinas': disciplinas,
        'status_final': status_final,
        'mostrar_reinscricao': mostrar_reinscricao,
        'realizou_prova_2024': False,
        'disciplinas_pendentes_nomes': list(disciplinas_pendentes.keys()),
        'anos_disponiveis': anos_disponiveis,
        'ano_selecionado': ano_selecionado,
        'ano_selecionado_int': ano_selecionado_int,
        'mostrar_botao_impressao': mostrar_botao_impressao,
    }

    return render(request, 'painel_candidato.html', context)




################################################################################################################################################

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import uuid
from .models import Registro
from django.core.mail import send_mail


@csrf_exempt
def verifica_email_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print("➡️ Recebido pedido de reset para:", email)

        # Busca o registro mais recente com esse e-mail
        registro = (
            Registro.objects
            .filter(email=email)
            .order_by('-ano_exame')
            .first()
        )

        if not registro:
            print("❌ Nenhum usuário encontrado com este e-mail:", email)
            return JsonResponse({'status': 'erro'}, status=400)

        # Gera novo token e define validade de 1 hora
        novo_token = uuid.uuid4()
        registro.token_recuperacao = novo_token
        registro.token_expira_em = timezone.now() + timedelta(hours=1)

        try:
            registro.save(update_fields=['token_recuperacao', 'token_expira_em'])
            print(f"✅ Token salvo com sucesso: {novo_token}")
        except Exception as e:
            print(f"❌ Erro ao salvar token no banco: {e}")
            return JsonResponse({'status': 'erro_banco'}, status=500)

        # Monta o link real de redefinição
        reset_url = f"http://{request.get_host()}/redefinir-senha/{novo_token}/"

        try:
            send_mail(
                subject='Recuperação de Senha - Suplência SEMED',
                message=f'Olá, {registro.nome}.\n\nClique no link a seguir para redefinir sua senha:\n\n{reset_url}\n\nEste link expira em 1 hora.',
                from_email='nao-responder@semed.gov.br',
                recipient_list=[email],
                fail_silently=False,
            )
            print("✅ E-mail enviado com sucesso para:", email)
        except Exception as e:
            print("❌ Erro ao enviar e-mail:", e)
            return JsonResponse({'status': 'erro_envio'}, status=500)

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'erro': 'Método não permitido'}, status=405)



################################################################################################################################################

from django.db.models import Min
from django.http import JsonResponse
from .models import Bairro

def get_bairros(request):
    bairros = (
        Bairro.objects
        .values('bairro_distrito')
        .annotate(id=Min('id'))  # pega o menor id por bairro
        .order_by('bairro_distrito')  # ordena alfabeticamente
    )
    return JsonResponse({'bairros': list(bairros)})

################################################################################################################################################

def redefinir_senha_view(request, token):
    try:
        # Pega o registro mais recente com esse token
        registro = Registro.objects.filter(token_recuperacao=token).order_by('-ano_exame').first()
        if not registro:
            return render(request, 'redefinir_senha_expirado.html')
    except Registro.DoesNotExist:
        return render(request, 'redefinir_senha_expirado.html')

    if not registro.token_esta_valido():
        return render(request, 'redefinir_senha_expirado.html')

    if request.method == 'POST':
        nova_senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if nova_senha and nova_senha == confirmar_senha:
            # Atualiza todos os registros com esse CPF
            registros = Registro.objects.filter(cpf=registro.cpf)
            for r in registros:
                r.senha = make_password(nova_senha)
                r.token_recuperacao = None
                r.token_expira_em = None
                r.save(update_fields=['senha', 'token_recuperacao', 'token_expira_em'])

            print("✅ Senha redefinida e sincronizada com todos os registros.")
            return render(request, 'redefinir_senha_sucesso.html')
        else:
            return render(request, 'redefinir_senha_form.html', {
                'registro': registro,
                'erro': 'As senhas não coincidem.'
            })

    return render(request, 'redefinir_senha_form.html', {'registro': registro})

################################################################################################################################################

def editar_cadastro(request):
    candidato_id = request.session.get('candidato_id')
    if not candidato_id:
        return redirect('login_candidato')

    candidato = get_object_or_404(Registro, id=candidato_id)

    if request.method == 'POST':
        candidato.telefone = request.POST.get('telefone')
        candidato.endereco = request.POST.get('endereco')
        # Atualize outros campos se necessário
        candidato.save()
        return redirect('painel_candidato')

    return render(request, 'editar_cadastro.html', {'candidato': candidato})
################################################################################################################################################

def progresso_inscricao_view(request):
    candidato_id = request.session.get('candidato_id')
    if not candidato_id:
        return redirect('login_candidato')

    candidato = get_object_or_404(Registro, id=candidato_id)

    # Mapeamento das disciplinas e notas
    disciplinas = {
        'Português': candidato.portugues,
        'Matemática': candidato.matematica,
        'História': candidato.historia,
        'Geografia': candidato.geografia,
        'Ciências': candidato.ciencias,
        'Arte': candidato.arte,
        'Inglês': candidato.ingles,
        'Educação Física': candidato.ed_fisica,
        'Redação': candidato.redacao,
        'Média Linguagens': candidato.media_ling,
    }

    # Classificação das disciplinas
    disciplinas_aprovadas = {nome: nota for nome, nota in disciplinas.items() if nota is not None and nota >= 5.0}
    disciplinas_pendentes = {nome: nota for nome, nota in disciplinas.items() if nota is None or nota < 5.0}

    return render(request, 'progresso_inscricao.html', {
        'candidato': candidato,
        'disciplinas_aprovadas': disciplinas_aprovadas,
        'disciplinas_pendentes': disciplinas_pendentes,
    })
################################################################################################################################################


from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.templatetags.static import static
import qrcode
from io import BytesIO
import base64
import weasyprint
from .models import Registro

def imprimir_inscricao_pdf(request, id):
    candidato = get_object_or_404(Registro, id=id)

    # Define data e horário padrão se não estiverem preenchidos
    if not candidato.data_prova:
        candidato.data_prova = datetime(2025, 10, 19, 7, 30)

    # Geração do QR Code
    dados_qr = f"ID: {candidato.id} | CPF: {candidato.cpf} | Nome: {candidato.nome}"
    qr = qrcode.make(dados_qr)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    qrcode_url = f"data:image/png;base64,{qr_base64}"

    # Caminhos das imagens (cabeçalho e rodapé)
    cabecalho_url = request.build_absolute_uri(static('assets/dist/img/cabecalho.png'))
    rodape_url = request.build_absolute_uri(static('assets/dist/img/rodape.png'))

    # Conversão das disciplinas de string para lista (caso não seja "todas")
    disciplinas_list = []
    if candidato.prova_todas_disciplinas != "Sim" and candidato.disciplinas:
        disciplinas_list = [d.strip() for d in candidato.disciplinas.split(',') if d.strip()]

    # Renderiza HTML
    template = get_template('pdf/ficha_inscricao_pdf.html')
    html = template.render({
        'candidato': candidato,
        'qrcode_url': qrcode_url,
        'cabecalho_url': cabecalho_url,
        'rodape_url': rodape_url,
        'disciplinas_list': disciplinas_list,
    })

    # Gera o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="inscricao_{candidato.cpf}.pdf"'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response

################################################################################################################################################

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
import re
from .models import CustomUser, Registro

def login_candidato_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        cpf = request.POST.get('cpf', '').strip()
        senha = request.POST.get('password', '').strip()

        # Validação básica
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            messages.error(request, 'CPF inválido. Use o formato 000.000.000-00.')
            return render(request, 'login_candidato.html')

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messages.error(request, 'E-mail inválido.')
            return render(request, 'login_candidato.html')

        if not senha:
            messages.error(request, 'Senha não informada.')
            return render(request, 'login_candidato.html')

        # Tentativa como admin (CustomUser)
        try:
            admin = CustomUser.objects.get(email=email, cpf=cpf)
            if admin.check_password(senha):
                auth_login(request, admin)
                request.session['logged_in'] = True
                return redirect('dashboard')
            else:
                messages.error(request, 'Senha incorreta para administrador.')
        except CustomUser.DoesNotExist:
            pass  # Não encontrado como admin

        # Tentativa como candidato
        try:
            candidato = Registro.objects.get(cpf=cpf, email=email)
            if check_password(senha, candidato.senha):
                request.session['candidato_id'] = candidato.id
                return redirect('painel_candidato')
            else:
                messages.error(request, 'Senha incorreta.')
        except Registro.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

    return render(request, 'login_candidato.html')

################################################################################################################################################

import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import CustomUser

def login_admin(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf', '').strip()
        senha = request.POST.get('password', '').strip()
        user_type = request.POST.get('user_type', '').strip()

        print("🔍 CPF:", cpf)
        print("🔍 Tipo:", user_type)

        # Validação do CPF com máscara
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            messages.error(request, 'CPF inválido. Use o formato 000.000.000-00.')
            return render(request, 'login_admin.html')

        if not senha:
            messages.error(request, 'Senha não informada.')
            return render(request, 'login_admin.html')

        try:
            user = CustomUser.objects.get(cpf=cpf, tipo=user_type, is_active=True)
            print("✅ Usuário encontrado:", user.email)

            if check_password(senha, user.password):
                print("🔐 Senha válida")
                request.session['admin_id'] = user.id
                request.session['logged_in'] = True
                request.session['user_type'] = user_type
                return redirect('dashboard')
            else:
                print("❌ Senha incorreta")
                messages.error(request, 'Senha incorreta.')
        except CustomUser.DoesNotExist:
            print("🚫 Usuário com CPF e tipo não encontrado")
            messages.error(request, 'Usuário não encontrado ou tipo incorreto.')

    return render(request, 'login_admin.html')


################################################################################################################################################

def gerar_ficha(request, candidato_id):
    candidato = Registro.objects.get(id=candidato_id)
    
    # Dados que serão codificados no QR
    dados_qr = f'{candidato.nome} | CPF: {candidato.cpf} | ID: {candidato.id}'
    
    qr = qrcode.make(dados_qr)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    qrcode_url = f'data:image/png;base64,{img_base64}'

    return render(request, 'ficha_inscricao.html', {
        'candidato': candidato,
        'qrcode_url': qrcode_url
    })
################################################################################################################################################

def ficha_inscricao_view(request, candidato_id):
    candidato = Registro.objects.get(id=candidato_id)

    # Gera QR Code com informações básicas
    dados_qr = f"ID: {candidato.id} | CPF: {candidato.cpf} | Nome: {candidato.nome}"
    qr = qrcode.make(dados_qr)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    qrcode_url = f"data:image/png;base64,{qr_base64}"

    return render(request, "ficha_inscricao.html", {
        "candidato": candidato,
        "qrcode_url": qrcode_url
    })
################################################################################################################################################

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Pode remover em produção
def formulario_reinscricao(request):
    candidato_id = request.session.get('candidato_id')
    if not candidato_id:
        return redirect('login_candidato')

    candidato = get_object_or_404(Registro, id=candidato_id)

    # Descobre disciplinas pendentes
    disciplinas_pendentes = {
        "Português": candidato.portugues,
        "Matemática": candidato.matematica,
        "Ciências": candidato.ciencias,
        "Arte": candidato.arte,
        "Educação Física": candidato.ed_fisica,
        "História": candidato.historia,
        "Geografia": candidato.geografia,
        "Inglês": candidato.ingles,
    }
    disciplinas_pendentes = {k: v for k, v in disciplinas_pendentes.items() if v is None or v < 7.0}

    context = {
        'candidato': candidato,
        'disciplinas_pendentes': disciplinas_pendentes,
    }
    return render(request, 'formulario_reinscricao.html', context)
################################################################################################################################################

@csrf_exempt
def salvar_reinscricao(request):
    if request.method == 'POST':
        candidato_id = request.session.get('candidato_id')
        if not candidato_id:
            return redirect('login_candidato')

        candidato = get_object_or_404(Registro, id=candidato_id)

        disciplinas_selecionadas = ", ".join(request.POST.getlist('disciplinas[]'))
        candidato.disciplinas = disciplinas_selecionadas
        candidato.save()

        return redirect('painel_candidato')
################################################################################################################################################

def formulario_reinscricao_view(request):
    candidato_id = request.session.get('candidato_id')
    if not candidato_id:
        return redirect('login_candidato')

    candidato = get_object_or_404(Registro, id=candidato_id)

    disciplinas = {
        "Português": candidato.portugues,
        "Matemática": candidato.matematica,
        "Ciências": candidato.ciencias,
        "Arte": candidato.arte,
        "Educação Física": candidato.ed_fisica,
        "História": candidato.historia,
        "Geografia": candidato.geografia,
        "Inglês": candidato.ingles,
    }

    disciplinas_pendentes = [nome for nome, nota in disciplinas.items() if nota is None or nota < 7.0]

    if request.method == 'POST':
        # Mesmo processamento de cadastro original, mas atualiza o mesmo `Registro` ou cria um novo se quiser separação
        # Aqui você pode decidir sobrescrever o atual ou criar um novo Registro com `tipo='reinscricao'`
        pass  # preencha conforme sua regra de negócio

    return render(request, 'webapp/formulario_reinscricao.html', {
        'candidato': candidato,
        'disciplinas': Disciplina.objects.filter(ativo=True),
        'disciplinas_pendentes': disciplinas_pendentes,
    })
################################################################################################################################################

from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from .models import Registro, Bairro
from datetime import datetime
from .utils import gerar_numero_unico

@require_POST
def reinscrever_usuario(request):
    candidato_id = request.session.get('candidato_id')
    if not candidato_id:
        return redirect('login_candidato')

    candidato_anterior = get_object_or_404(Registro, id=candidato_id)

    # --- Marcar TODOS registros do CPF daquele ano anterior como reinscrito! (evita duplicidade do botão)
    Registro.objects.filter(
        cpf=candidato_anterior.cpf, 
        ano_exame=candidato_anterior.ano_exame
    ).update(reinscrito=True)

    # Trata o campo bairro com segurança
    bairro = None
    bairro_id = request.POST.get('bairro')
    if bairro_id:
        try:
            bairro = Bairro.objects.get(pk=bairro_id)
        except Bairro.DoesNotExist:
            bairro = None

    # Verifica a opção de prova de todas as disciplinas
    prova_todas = request.POST.get('prova_todas_disciplinas')

    # 🔒 Bloqueio explícito do valor "Sim"
    if prova_todas == "Sim":
        from django.contrib import messages
        messages.error(request, "A opção 'Sim' está desabilitada no momento.")
        return redirect('painel_candidato')

    # Valor default forçado é "Não"
    prova_todas = "Não"

    # Coleta das disciplinas (apenas se a opção for "Não")
    disciplinas = ",".join(request.POST.getlist('disciplinas[]'))

    # Aulões
    deseja_participar_aulao = request.POST.get('deseja_participar_aulao') or "Não"
    turnos_aulao = ",".join(request.POST.getlist('turnos_aulao[]')) if deseja_participar_aulao == "Sim" else ""

    # Criação do novo registro
    novo = Registro(
        nome=candidato_anterior.nome,
        email=request.POST.get('email'),
        cpf=candidato_anterior.cpf,
        data_nascimento=candidato_anterior.data_nascimento,
        telefone=request.POST.get('telefone'),
        telefone_2=request.POST.get('telefone_2'),
        cidade=request.POST.get('cidade'),
        endereco=request.POST.get('endereco'),
        bairro=bairro,
        escola_2024=request.POST.get('escola_2024'),
        local_prova=request.POST.get('local_prova'),
        fez_exame_supletivo=request.POST.get('fez_exame_supletivo') or "Não",
        ano_ultima_prova=request.POST.get('ano_ultima_prova') or None,
        possui_necessidade_especial="Sim" if request.POST.get('possui_necessidade_especial') == 'Sim' else "Não",
        necessidade_especial_detalhe=request.POST.get('necessidade_especial_detalhe'),
        prova_todas_disciplinas=prova_todas,
        disciplinas=disciplinas,
        deseja_participar_aulao=deseja_participar_aulao,
        turnos_aulao=turnos_aulao,
        nome_responsavel=request.POST.get('nome_responsavel'),
        cpf_responsavel=request.POST.get('cpf_responsavel'),
        rg_responsavel=request.POST.get('rg_responsavel'),
        tipo_responsavel=request.POST.get('tipo_responsavel'),
        senha=candidato_anterior.senha,
        ano_exame=datetime.now().year,
        reinscricao=True,
        reinscrito=False,
        numero=gerar_numero_unico(),
        status="Reinscrito",
    )

    # Se quiser copiar as notas aprovadas do registro anterior para o novo, use:
    campos_disciplinas = [
        'portugues', 'arte', 'ciencias', 'ed_fisica',
        'geografia', 'historia', 'ingles', 'matematica', 'media_ling', 'redacao'
    ]
    for campo in campos_disciplinas:
        nota = getattr(candidato_anterior, campo, None)
        if nota is not None and nota >= 7.0:
            setattr(novo, campo, nota)

    novo.save()
    request.session['candidato_id'] = novo.id

    return redirect('painel_candidato')





################################################################################################################################################

def listar_disciplinas_ajax(request):
    if request.method == 'GET':
        disciplinas = Disciplina.objects.filter(ativo=True).values('id', 'nome')
        return JsonResponse({'disciplinas': list(disciplinas)})
################################################################################################################################################

from django.http import JsonResponse
from .models import Disciplina

def disciplinas_json(request):
    disciplinas = Disciplina.objects.all().values('id', 'nome')
    return JsonResponse(list(disciplinas), safe=False)
################################################################################################################################################

# def listar_disciplinas_json(request):
#     disciplinas = Disciplina.objects.all().values('id', 'nome')
#     return JsonResponse(list(disciplinas), safe=False)
################################################################################################################################################

# webapp/views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Registro
from webapp.models import Bairro  # Certifique-se de que está correto o caminho

def atualizar_registro(request):
    if request.method == "POST":
        registro_id = request.POST.get('id')
        registro = get_object_or_404(Registro, id=registro_id)

        # Campos simples
        registro.nome = request.POST.get('nome')
        registro.email = request.POST.get('email')
        registro.cpf = request.POST.get('cpf')
        registro.data_nascimento = request.POST.get('data_nascimento')
        registro.telefone = request.POST.get('telefone')
        registro.telefone_2 = request.POST.get('telefone_2')
        registro.cidade = request.POST.get('cidade')
        registro.endereco = request.POST.get('endereco')

        # Trata o campo bairro como ForeignKey com segurança
        bairro_id = request.POST.get('bairro')
        try:
            registro.bairro = Bairro.objects.get(id=bairro_id)
        except Bairro.DoesNotExist:
            registro.bairro = None  # ou mensagens.warning(request, "Bairro inválido")

        registro.maior_de_18 = request.POST.get('maior_de_18')
        registro.nome_responsavel = request.POST.get('nome_responsavel')
        registro.cpf_responsavel = request.POST.get('cpf_responsavel')
        registro.rg_responsavel = request.POST.get('rg_responsavel')
        registro.tipo_responsavel = request.POST.get('tipo_responsavel')
        registro.prova_todas_disciplinas = request.POST.get('prova_todas_disciplinas')
        registro.fez_exame_supletivo = request.POST.get('fez_exame_supletivo')
        registro.possui_necessidade_especial = request.POST.get('possui_necessidade_especial')
        registro.necessidade_especial_detalhe = request.POST.get('necessidade_especial_detalhe')
        registro.local_prova = request.POST.get('local_prova')
        registro.data_prova = request.POST.get('data_prova')
        registro.escola_2024 = request.POST.get('escola_2024')

        # Senha (opcional)
        senha = request.POST.get('senha')
        confirmar = request.POST.get('confirmar_senha')
        if senha and senha == confirmar:
            registro.senha = make_password(senha)

        registro.save()
        messages.success(request, "Dados atualizados com sucesso.")
        return redirect('painel_candidato')

    messages.error(request, "Requisição inválida.")
    return redirect('painel_candidato')

################################################################################################################################################

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from webapp.models import CustomUser

@csrf_exempt
@require_POST
@never_cache
def ajax_admin_password_reset(request):
    form = PasswordResetForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = CustomUser.objects.filter(email=email, is_active=True).first()

        if user:
            from_email = 'noreply@semed.com.br'
            current_site = get_current_site(request)
            context = {
                'email': user.email,
                'domain': current_site.domain,
                'site_name': 'SEMED',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            }

            subject = render_to_string('admin_password_reset_subject.txt', context)
            subject = ''.join(subject.splitlines())

            message = render_to_string('admin_password_reset_email.html', context)

            user.email_user(subject, message, from_email=from_email)
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
################################################################################################################################################

from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'admin_password_reset_confirm.html'
    success_url = reverse_lazy('login')
    login_url = reverse_lazy('login')  # <- ESSENCIAL para evitar redirecionamento para /admin/login


    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
################################################################################################################################################


from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from .models import Escola  # ajuste conforme seu app/modelo

@require_POST
def buscar_escolas(request):
    data = json.loads(request.body)
    endereco = data.get("endereco", "")
    bairro = data.get("bairro", "")
    cep = data.get("cep", "")

    escolas = Escola.objects.all()

    if endereco:
        escolas = escolas.filter(endereco__icontains=endereco)
    if bairro:
        escolas = escolas.filter(bairro__icontains=bairro)
    if cep:
        escolas = escolas.filter(cep__icontains=cep)

    resultado = [{
        "nome": e.nome,
        "endereco": e.endereco,
        "bairro": e.bairro,
        "cep": e.cep
    } for e in escolas]

    return JsonResponse({"escolas": resultado})
################################################################################################################################################


def servicos(request):
    return render(request, 'servicos.html')
################################################################################################################################################


from django.shortcuts import render, get_object_or_404, redirect
from .models import Registro

def visualizar_aluno(request, pk):
    aluno = get_object_or_404(Registro, pk=pk)
    return render(request, 'webapp/visualizar_aluno.html', {'aluno': aluno})
################################################################################################################################################

from django.shortcuts import render, get_object_or_404, redirect
from .models import Registro, Bairro

def editar_aluno(request, pk):
    aluno = get_object_or_404(Registro, pk=pk)
    bairros = Bairro.objects.all()

    if request.method == 'POST':
        # Atribui os campos do formulário
        aluno.nome = request.POST.get('nome')
        aluno.cpf = request.POST.get('cpf')
        aluno.data_nascimento = request.POST.get('data_nascimento') or None
        aluno.email = request.POST.get('email')
        aluno.telefone = request.POST.get('telefone')
        aluno.telefone_2 = request.POST.get('telefone_2')
        aluno.endereco = request.POST.get('endereco')
        aluno.cidade = request.POST.get('cidade')
        aluno.escola_2024 = request.POST.get('escola_2024')
        aluno.ano_exame = request.POST.get('ano_exame') or None
        aluno.local_prova = request.POST.get('local_prova')

        # Notas
        for campo in ['portugues', 'redacao', 'ingles', 'arte', 'ed_fisica', 'historia', 'geografia', 'matematica', 'ciencias']:
            setattr(aluno, campo, request.POST.get(campo) or 0)

        aluno.status = request.POST.get('status')
        aluno.materias_aprovadas = request.POST.get('materias_aprovadas')
        aluno.observacao = request.POST.get('observacao')
        aluno.fez_exame_supletivo = request.POST.get('fez_exame_supletivo')
        aluno.prova_todas_disciplinas = request.POST.get('prova_todas_disciplinas')

        aluno.possui_necessidade_especial = request.POST.get('possui_necessidade_especial')
        aluno.necessidade_especial_detalhe = request.POST.get('necessidade_especial_detalhe')

        aluno.nome_responsavel = request.POST.get('nome_responsavel')
        aluno.cpf_responsavel = request.POST.get('cpf_responsavel')
        aluno.rg_responsavel = request.POST.get('rg_responsavel')
        aluno.tipo_responsavel = request.POST.get('tipo_responsavel')
        aluno.maior_de_18 = bool(request.POST.get('maior_de_18'))

        # Bairro
        bairro_id = request.POST.get('bairro')
        aluno.bairro = Bairro.objects.get(id=bairro_id) if bairro_id else None

        aluno.save()
        print(f'Aluno {aluno.nome} atualizado com sucesso.')


        messages.success(request, "Dados atualizados com sucesso!")

        # ✅ Redireciona após salvar
        return redirect('visualizar_aluno', pk=aluno.pk)

    return render(request, 'webapp/editar_aluno.html', {
        'aluno': aluno,
        'bairros': bairros
    })
################################################################################################################################################


from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from .models import Registro
import io

def exportar_pdf_alunos(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Cabeçalho
    p.setFont("Helvetica-Bold", 14)
    p.drawString(2 * cm, height - 2 * cm, "Relatório Geral de Alunos - EJA")
    p.setFont("Helvetica", 10)
    p.drawString(2 * cm, height - 2.6 * cm, "Sistema de Gestão Educacional - SEMED")

    # Coleta de dados
    alunos = Registro.objects.all().order_by('nome')
    total_alunos = alunos.count()
    disciplinas = ['Português', 'Redação', 'Inglês', 'Arte', 'Educação Física', 'História', 'Geografia', 'Matemática', 'Ciências']
    disciplina_quantitativo = {disc: alunos.filter(disciplinas__icontains=disc).count() for disc in disciplinas}

    # Totais
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2 * cm, height - 4 * cm, f"Total de Alunos: {total_alunos}")
    p.setFont("Helvetica-Bold", 11)
    p.drawString(2 * cm, height - 5 * cm, "Distribuição por Disciplinas:")

    y = height - 5.6 * cm
    p.setFont("Helvetica", 10)
    for d, q in disciplina_quantitativo.items():
        p.drawString(2.5 * cm, y, f"- {d}: {q}")
        y -= 0.5 * cm

    # Tabela de alunos
    y -= 0.5 * cm
    p.setFont("Helvetica-Bold", 10)
    p.drawString(2 * cm, y, "Alunos Cadastrados:")
    y -= 0.7 * cm

    p.setFont("Helvetica", 9)
    for aluno in alunos:
        if y < 3 * cm:
            p.showPage()
            y = height - 2 * cm
        p.drawString(2 * cm, y, f"{aluno.nome} | CPF: {aluno.cpf} | Escola: {aluno.escola_2024} | Ano: {aluno.ano_exame}")
        y -= 0.5 * cm

    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
################################################################################################################################################


from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from .models import Registro
from django.db.models import Q
from datetime import datetime

def gerar_pdf_relatorio(request):
    busca = request.GET.get('busca', '')
    ano_exame = request.GET.get('ano_exame', '')

    alunos = Registro.objects.all()

    if busca:
        alunos = alunos.filter(
            Q(nome__icontains=busca) |
            Q(cpf__icontains=busca) |
            Q(escola_2024__icontains=busca)
        )

    if ano_exame:
        alunos = alunos.filter(ano_exame=ano_exame)

    # Ajusta e normaliza disciplinas
    for aluno in alunos:
        disciplinas_raw = [d.strip() for d in aluno.disciplinas.split(',')] if aluno.disciplinas else []
        disciplinas_set = set(disciplinas_raw)

        # Substitui Redação e Média Linguagens por Português
        if {'Português', 'Redação', 'Média Linguagens'} & disciplinas_set:
            disciplinas_set -= {'Português', 'Redação', 'Média Linguagens'}
            disciplinas_set.add('Português')

        aluno.lista_disciplinas = sorted(disciplinas_set)

    # Contagem por disciplina (já considerando ajuste)
    disciplina_count = {}
    for aluno in alunos:
        for d in aluno.lista_disciplinas:
            disciplina_count[d] = disciplina_count.get(d, 0) + 1

    total_alunos = alunos.count()

    html_string = render_to_string('webapp/relatorio_alunos_eja.html', {
        'alunos': alunos,
        'total_alunos': total_alunos,
        'disciplinas': disciplina_count,
        'data_geracao': datetime.now().strftime('%d/%m/%Y %H:%M')
    })

    pdf_file = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_eja.pdf"'
    return response



################################################################################################################################################



from django.shortcuts import render
from .models import Registro

def dashboard_eja_view(request):
    ano_exame = request.GET.get('ano_exame', '')

    # Aplica filtro por ano, se selecionado
    if ano_exame:
        registros = Registro.objects.filter(ano_exame=ano_exame)
    else:
        registros = Registro.objects.all()

    total = registros.count()
    aprovados = registros.filter(status='aprovado').count()
    reprovados = registros.filter(status='reprovado').count()
    concluintes = registros.filter(status='concluinte').count()

    percentual_aprovados = (aprovados / total) * 100 if total else 0
    percentual_reprovados = (reprovados / total) * 100 if total else 0
    percentual_concluintes = (concluintes / total) * 100 if total else 0

    anos_disponiveis = Registro.objects.values_list('ano_exame', flat=True).distinct().order_by('-ano_exame')

    context = {
        'total': total,
        'aprovados': aprovados,
        'reprovados': reprovados,
        'concluintes': concluintes,
        'percentual_aprovados': round(percentual_aprovados, 2),
        'percentual_reprovados': round(percentual_reprovados, 2),
        'percentual_concluintes': round(percentual_concluintes, 2),
        'anos_disponiveis': anos_disponiveis,
        'ano_exame': ano_exame,
    }

    return render(request, 'dashboard_eja.html', context)
################################################################################################################################################


from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit  # ou xhtml2pdf, weasyprint, etc.

def gerar_atestado_view(request, registro_id):
    from .models import Registro
    registro = Registro.objects.get(pk=registro_id)

    if request.method == 'POST':
        rg = request.POST.get('rg')
        data_nascimento = request.POST.get('dataNascimento')
        cidade_nascimento = request.POST.get('cidadeNascimento')
        nome_pai = request.POST.get('nomePai')
        nome_mae = request.POST.get('nomeMae')

        html = render_to_string('pdfs/atestado_template.html', {
            'registro': registro,
            'rg': rg,
            'data_nascimento': data_nascimento,
            'cidade_nascimento': cidade_nascimento,
            'nome_pai': nome_pai,
            'nome_mae': nome_mae
        })

        pdf = pdfkit.from_string(html, False)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="atestado.pdf"'
        return response
################################################################################################################################################

from django.shortcuts import render
from .models import Registro

def relatorio_view(request):
    ano_exame = request.GET.get('ano_exame', '').strip()

    if ano_exame.isdigit():
        registros = Registro.objects.filter(ano_exame=int(ano_exame))
    else:
        registros = Registro.objects.all()

    anos_disponiveis = (
        Registro.objects.exclude(ano_exame__isnull=True)
        .values_list('ano_exame', flat=True)
        .distinct()
        .order_by('-ano_exame')
    )

    context = {
        'titulo': 'Relatórios EJA',
        'descricao': 'Relatórios de desempenho e análises do EJA.',
        'registros': registros,
        'anos_disponiveis': anos_disponiveis,
        'ano_exame': ano_exame,  # ✅ nome exato que o template espera
    }

    return render(request, 'webapp/relatorios_eja.html', context)
################################################################################################################################################

from django.shortcuts import render
from .models import Registro

def auloes_candidatos(request):
    candidatos = Registro.objects.filter(deseja_participar_aulao='Sim').order_by('-id')
    turnos = {'Matutino': 0, 'Vespertino': 0, 'Noturno': 0}
    for c in candidatos:
        c.turnos_lista = [t.strip() for t in (c.turnos_aulao or "").split(",") if t.strip()]
        if c.turnos_aulao:
            turnos_str = c.turnos_aulao.split(',')
            c.turnos_lista = [t.strip() for t in turnos_str]
            for t in c.turnos_lista:
                if t in turnos:
                    turnos[t] += 1
        else:
            c.turnos_lista = []
    return render(request, 'auloes_candidatos.html', {
        'candidatos': candidatos,
        'turnos': turnos,
        'total': candidatos.count()
    })


################################################################################################################################################