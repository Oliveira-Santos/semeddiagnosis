from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    aluno_matematica_view,
    get_diagnose_data_inic_alunos_matematica,
    upload_excel_aluno_matematica
)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import gestao_arquivos_view

from .views import gerar_relatorio_completo_view

from .views import emitir_atestado_view

from .views import get_diagnose_data_matematica

from webapp.views import verifica_email_reset

from .views import disciplinas_json

from .views import ajax_admin_password_reset

from django.urls import reverse_lazy

from .views import CustomPasswordResetConfirmView



urlpatterns = [
    path('', views.index_view, name='index'),  # página principal
    # User Authentication and Management
    path('', views.home_view, name='home'),  # Aqui o nome 'home' é definido
    path('', views.BASE, name='BASE'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('create-superuser/', views.create_superuser, name='create_superuser'),
    path('base/', views.base_view, name='base'),

    # Uploads and Skills Visualization
    path('habilidades/', views.habilidades_view, name='habilidades'),
    path('habilidades2/', views.habilidades2_view, name='habilidades2'),
    path('upload_habilidades/', views.upload_excel, name='upload_habilidades'),
    path('habilidades4/', views.habilidades4_view, name='habilidades4'),
    path('upload_habilidades2/', views.upload_habilidades2, name='upload_habilidades2'),
    path('upload_habilidades4/', views.upload_habilidades4, name='upload_habilidades4'),

    # Língua Portuguesa Professores
    path('lingua-portuguesa-professores/', views.lingua_portuguesa_prof_view, name='lingua_portuguesa_prof_view'),
    path('get-diagnose-data/', views.get_diagnose_data, name='get_diagnose_data'),

    # Matemática Professores Anos Iniciais
    path('lingua-matematica-prof/', views.lingua_matematica_prof_view, name='lingua_matematica_prof_view'),
    path('get_diagnose_data_matematica/', views.get_diagnose_data_matematica, name='get_diagnose_data_matematica'),

    # Língua Portuguesa Professores Anos Finais
    path('lingua-portuguesa-professores-finais/', views.lingua_portuguesa_prof_finais_view, name='lingua_portuguesa_prof_finais_view'),
    path('get-diagnose-data-portugues-finais/', views.get_diagnose_data_portugues_finais, name='get_diagnose_data_portugues_finais'),

    # Matemática Professores Anos Finais
    path('matematica-professores-finais/', views.matematica_prof_finais_view, name='matematica_prof_finais_view'),
    path('get-diagnose-data-matematica-finais/', views.get_diagnose_data_matematica_finais, name='get_diagnose_data_matematica_finais'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('upload_excel/aluno_portugues/', views.upload_excel_aluno_portugues, name='upload_excel_aluno_portugues'),
    path('alunos-portugues/', views.aluno_portugues_view, name='aluno_portugues_view'),
    path('get-diagnose-data-inic-alunos-port/', views.get_diagnose_data_inic_alunos_port, name='get_diagnose_data_inic_alunos_port'),

    path('upload-habilidades/', views.upload_habilidades2, name='upload_habilidades_view'),
    path('habilidades-matematica/', views.visualizar_habilidades_matematica, name='visualizar_habilidades_matematica'),
    path('habilidades-portugues/', views.visualizar_habilidades_portugues, name='visualizar_habilidades_portugues'),
    path('habilidades/matematica/', views.habilidades_matematica_view, name='habilidades_matematica_view'),
    path('habilidades/portugues/', views.habilidades_portugues_view, name='habilidades_portugues_view'),

    path('upload-habilidades-matematica/', views.upload_habilidades_matematica_view, name='upload_habilidades_matematica_view'),
    path('upload-habilidades-portugues/', views.upload_habilidades_portugues_view, name='upload_habilidades_portugues_view'),

    path('matematica-aluno/', aluno_matematica_view, name='aluno_matematica_view'),
    path('matematica-aluno/dados/', get_diagnose_data_inic_alunos_matematica, name='get_diagnose_data_inic_alunos_matematica'),
    path('matematica-aluno/upload/', upload_excel_aluno_matematica, name='upload_excel_aluno_matematica'),
    path('matematica-aluno/', views.matematica_aluno_view, name='matematica_aluno_view'),
    
    path('search/', views.search_view, name='search_view'),

    path('ajuda/', views.ajuda, name='ajuda'),
    path('solicitar-suporte/', views.solicitar_suporte, name='solicitar_suporte'),
    path('feedback-suporte/', views.feedback_suporte, name='feedback_suporte'),

    path('ajuda/', views.ajuda_view, name='ajuda_view'),

    path('seguranca/', views.seguranca_view, name='seguranca_view'),

    path('alterar-senha/', views.alterar_senha_view, name='alterar_senha'),

    path('configurar-notificacoes/', views.configurar_notificacoes_view, name='configurar_notificacoes'),

    path('upload/', views.upload_exame_view, name='upload_exame'),
    path('gestao-arquivos/', views.gestao_arquivos_view, name='gestao_arquivos'),

    path('editar/<int:id>/', views.editar_registro_view, name='editar_registro'),
    path('excluir/<int:id>/', views.excluir_registro_view, name='excluir_registro'),  # Adicione esta linha

    path('gestao/', gestao_arquivos_view, name='gestao_arquivos'),

     path('relatorios/pdf/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
     path('gerar_relatorio_completo/', gerar_relatorio_completo_view, name='gerar_relatorio_completo'),

    #  path('configurar_certificados/', configurar_certificados_view, name='configurar_certificados'),

    path('emitir-certificado/<int:id>/', views.emitir_certificado_view, name='emitir_certificado'),
    path('emitir-atestado/<int:id>/', views.emitir_atestado_view, name='emitir_atestado'),

    path('gerar-atestado/<int:id>/', emitir_atestado_view, name='gerar_atestado'),

    path('get-diagnose-data-matematica/', get_diagnose_data_matematica, name='get_diagnose_data_matematica'),

    path('eja/alunos/', views.lista_alunos_eja, name='alunos_eja'),

    path('inscricao/', views.formulario_inscricao, name='formulario_inscricao'),

    path('cadastro/', views.cadastro_usuario_view, name='cadastro_usuario'),
   
    path('login-candidato/', views.login_candidato, name='login_candidato'),

    path('get-bairros/', views.get_bairros, name='get_bairros'),

    path('redefinir-senha/<uuid:token>/', views.redefinir_senha_view, name='redefinir_senha'),

    path('verifica-email-reset/', views.verifica_email_reset, name='verifica_email_reset'),

    # urls.py
    path('login-candidato/', views.login_candidato, name='login_candidato'),
    path('painel-candidato/', views.painel_candidato, name='painel_candidato'),

    path('editar-cadastro/', views.editar_cadastro, name='editar_cadastro'),

    path('progresso-inscricao/', views.progresso_inscricao_view, name='progresso_inscricao'),

    path('imprimir-inscricao/<int:id>/', views.imprimir_inscricao_pdf, name='imprimir_inscricao'),

    path('imprimir-inscricao/<int:id>/', views.imprimir_inscricao_pdf, name='imprimir_inscricao_pdf'),

    # path('login/', views.login_candidato_admin, name='login_candidato_admin'),

    path('login/', views.login_admin, name='login'),  # login do sistema geral
    path('login/candidato/', views.login_candidato, name='login_candidato'),  # login do candidato

     path('verificar-cpf/', views.verificar_cpf_ajax, name='verificar_cpf_ajax'),  # <- ESSA LINHA CORRIGE

    path('verificar-cpf/', views.verificar_cpf, name='verificar_cpf'),

    path('verificar-cpf-admin/', views.verificar_cpf_admin, name='verificar_cpf_admin'),

    path('url-para-listar-disciplinas/', views.listar_disciplinas, name='listar_disciplinas'),

    path('disciplinas-json/', views.listar_disciplinas, name='listar_disciplinas'),

    path('reinscricao/<str:cpf>/', views.reinscricao_usuario, name='reinscricao_usuario'),
    path('reinscricao/', views.formulario_reinscricao, name='formulario_reinscricao'),

    path('salvar-reinscricao/', views.salvar_reinscricao, name='salvar_reinscricao'),

    path('reinscrever/', views.reinscrever_usuario, name='reinscrever_usuario'),

    path('url-para-listar-disciplinas/', views.listar_disciplinas_ajax, name='listar_disciplinas_ajax'),

    path('disciplinas-json/', disciplinas_json, name='disciplinas_json'),

    path('atualizar-registro/', views.atualizar_registro, name='atualizar_registro'),


    # path('recuperar-senha/', auth_views.PasswordResetView.as_view(
    #     template_name='admin_password_reset.html',
    #     email_template_name='admin_password_reset_email.html',
    #     subject_template_name='admin_password_reset_subject.txt'
    # ), name='password_reset'),

    # path('recuperar-senha/enviado/', auth_views.PasswordResetDoneView.as_view(
    #     template_name='admin_password_reset_done.html'
    # ), name='password_reset_done'),

    # path('recuperar-senha/confirmar/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # path('recuperar-senha/completo/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name='admin_password_reset_complete.html'
    # ), name='password_reset_complete'),

    path('recuperar-senha-admin/', views.ajax_admin_password_reset, name='ajax_admin_password_reset'),

    path("buscar-escolas/", views.buscar_escolas, name="buscar_escolas"),

    path('servicos/', views.servicos, name='servicos'),

    path('aluno/<int:pk>/ver/', views.visualizar_aluno, name='visualizar_aluno'),


     path('eja/alunos/', views.lista_alunos_eja, name='lista_alunos_eja'),

    path('aluno/<int:pk>/editar/', views.editar_aluno, name='editar_aluno'),

    # urls.py
    # path('exportar/pdf/alunos/', views.exportar_pdf_alunos, name='exportar_pdf_alunos'),

    # urls.py
    path('relatorio/pdf/', views.gerar_pdf_relatorio, name='gerar_pdf_relatorio'),

    path('dashboard-eja/', views.dashboard_eja_view, name='dashboard_eja'),

    path('gerar-atestado/<int:registro_id>/', views.gerar_atestado_view, name='gerar_atestado'),

    path('relatorios_eja/', views.relatorio_view, name='relatorios_eja'),
    path(
            'recuperar-senha/',
            auth_views.PasswordResetView.as_view(
                template_name='admin_password_reset.html',
                email_template_name='admin_password_reset_email.html',
                subject_template_name='admin_password_reset_subject.txt',
                success_url=reverse_lazy('password_reset_done')
            ),
            name='password_reset'
        ),

        path(
            'recuperar-senha/enviado/',
            auth_views.PasswordResetDoneView.as_view(
                template_name='password_reset_done.html'
            ),
            name='password_reset_done'
        ),

        path(
            'reset/<uidb64>/<token>/',
            CustomPasswordResetConfirmView.as_view(),
            name='password_reset_confirm'
        ),











]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)