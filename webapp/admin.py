from django.contrib import admin
from .models import DiagnoseAlunoPortugues
from .models import Registro

admin.site.register(DiagnoseAlunoPortugues)


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'status', 'certificado_emitido', 'atestado_emitido')
    list_filter = ('status', 'certificado_emitido', 'atestado_emitido')


from django.contrib import admin
from .models import Candidato

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'email', 'status', 'data_prova')
    search_fields = ('nome_completo', 'cpf', 'email')
