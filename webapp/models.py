from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    USER_TYPE_CHOICES = (
        ('admin', 'Administrador'),
        ('gabinete', 'Gabinete'),
        ('dide', 'Dide'),
        ('diagnose', 'Diágnosis'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username

# =============================================
# Modelos de Língua Portuguesa anos iniciais
# =============================================
class Habilidade(models.Model):
    habilidade = models.CharField(max_length=10)
    nome_habilidade = models.CharField(max_length=255)
    seguimento = models.CharField(max_length=50)
    disciplina = models.CharField(max_length=50)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para armazenar a descrição da habilidade

    prof_401 = models.IntegerField()
    prof_403 = models.IntegerField()
    prof_404 = models.IntegerField()
    prof_406 = models.IntegerField()
    prof_408 = models.IntegerField()
    prof_409 = models.IntegerField()
    prof_410 = models.IntegerField()
    prof_413 = models.IntegerField()
    prof_414 = models.IntegerField()
    prof_415 = models.IntegerField()
    prof_417 = models.IntegerField()
    prof_421 = models.IntegerField()
    prof_423 = models.IntegerField()
    prof_426 = models.IntegerField()
    prof_428 = models.IntegerField()
    prof_429 = models.IntegerField()
    prof_430 = models.IntegerField()
    prof_431 = models.IntegerField()
    prof_432 = models.IntegerField()
    prof_433 = models.IntegerField()
    prof_434 = models.IntegerField()
    prof_435 = models.IntegerField()
    prof_436 = models.IntegerField()
    prof_437 = models.IntegerField()
    prof_438 = models.IntegerField()
    prof_439 = models.IntegerField()
    prof_441 = models.IntegerField()
    prof_442 = models.IntegerField()
    prof_447 = models.IntegerField()
    prof_451 = models.IntegerField()
    prof_471 = models.IntegerField()

    def __str__(self):
        return f"Habilidade {self.item} - {self.habilidade}"

class DiagnoseInicProfPort(models.Model):
    item = models.CharField(max_length=50)
    habilidade = models.CharField(max_length=255)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para armazenar a des

    # Campos para os números dos professores
    professor_401 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_403 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_404 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_406 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_408 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_409 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_410 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_413 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_414 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_415 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_417 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_421 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_423 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_426 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_428 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_429 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_430 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_431 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_432 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_433 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_434 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_435 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_436 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_437 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_438 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_439 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_441 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_442 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_447 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_451 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_471 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])

    def __str__(self):
        return f'Item {self.item} - {self.habilidade}'

# =============================================
# Modelos de Matemática anos iniciais
# =============================================
class DiagnoseMatematicaProf(models.Model):
    item = models.CharField(max_length=50)
    habilidade = models.CharField(max_length=255)

    # Campos para os números dos professores
    professor_300 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_301 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_302 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_305 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_306 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_308 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_310 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_317 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_318 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_319 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_320 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_323 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_324 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_328 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_329 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_330 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_331 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_333 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_338 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_339 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_341 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_342 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_343 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_344 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_345 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_346 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_347 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_348 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_350 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_351 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_352 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_353 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])
    professor_354 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')])

    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo agora movido para o final

    def __str__(self):
        return f'Item {self.item} - {self.habilidade}'


# =============================================
# Modelos de Língua Portuguesa anos finais
# =============================================
class DiagnoseAnosFinaisProfPort(models.Model):
    item = models.CharField(max_length=50)
    habilidade = models.CharField(max_length=255)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para armazenar a descrição da habilidade
    
    # Campos para os números dos professores com a opção "Branco"
    professor_101 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_102 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_103 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_104 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_105 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_106 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_107 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_109 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_110 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_112 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_114 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_117 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_119 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_120 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_121 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_124 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_126 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_128 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_129 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_130 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_131 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_134 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_135 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_137 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_138 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_139 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_140 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_142 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_143 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_144 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_145 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_146 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_147 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')
    professor_171 = models.CharField(max_length=7, choices=[('0', 'Erro'), ('1', 'Acerto'), ('Branco', 'Branco')], default='Branco')

    def __str__(self):
        return f'Item {self.item} - {self.habilidade}'
    


# =============================================
# Modelos de Língua Matemática anos finais
# =============================================
class DiagnoseAnosFinaisProfMat(models.Model):
    item = models.CharField(max_length=50)
    habilidade = models.CharField(max_length=255)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para a descrição da habilidade

    # Campos para os números dos professores (removendo 'Branco')
    professor_200 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_201 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_202 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_203 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_205 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_206 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_207 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_208 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_209 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_210 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_211 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_212 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_213 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_215 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_216 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_217 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_218 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_220 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_222 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_224 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_226 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_227 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_229 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_231 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_232 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_233 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_234 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_235 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_236 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_238 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_240 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_241 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')
    professor_243 = models.CharField(max_length=1, choices=[('N', 'Não'), ('S', 'Sim')], default='N')

    def __str__(self):
        return f'Item {self.item} - {self.habilidade}'

########################################################################################################################
#ALUNOS
########################################################################################################################
class DiagnoseAlunoPortugues(models.Model):
    SERIE_CHOICES = [
        ('3º', '3º Ano'),
        ('4º', '4º Ano'),
        ('5º', '5º Ano'),
        ('6º', '6º Ano'),
    ]
    
    tipo_usuario = models.CharField(max_length=20, choices=[('aluno', 'Aluno'), ('professor', 'Professor')])
    serie = models.CharField(max_length=10, choices=SERIE_CHOICES)
    habilidade = models.CharField(max_length=100)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para a descrição da habilidade
    acerto = models.FloatField()
    erro = models.FloatField()

    def clean(self):
        if not (0 <= self.acerto <= 1):
            raise ValidationError({'acerto': 'O valor de acerto deve estar entre 0 e 1.'})
        if not (0 <= self.erro <= 1):
            raise ValidationError({'erro': 'O valor de erro deve estar entre 0 e 1.'})

    def __str__(self):
        return f"{self.serie} - {self.habilidade}"
###################################################################################################################
# class HabilidadeMatematica(models.Model):
#     serie = models.CharField(max_length=50)
#     topico = models.CharField(max_length=255)
#     habilidade = models.CharField(max_length=255)
#     descricao = models.TextField()

#     def __str__(self):
#         return f'{self.serie} - {self.habilidade}'

# class HabilidadePortugues(models.Model):
#     serie = models.CharField(max_length=255)
#     topico = models.CharField(max_length=255)
#     habilidade = models.CharField(max_length=255)
#     descricao = models.TextField()

#     def __str__(self):
#         return f"{self.serie} - {self.habilidade}"
#########################################################################################################################
class DiagnoseAlunoMatematica(models.Model):
    SERIE_CHOICES = [
        ('3º', '3º Ano'),
        ('4º', '4º Ano'),
        ('5º', '5º Ano'),
        ('6º', '6º Ano'),
    ]
    
    tipo_usuario = models.CharField(max_length=20, choices=[('aluno', 'Aluno'), ('professor', 'Professor')])
    serie = models.CharField(max_length=10, choices=SERIE_CHOICES)
    habilidade = models.CharField(max_length=100)
    descricao_habilidade = models.TextField(null=True, blank=True)  # Campo para a descrição da habilidade
    acerto = models.FloatField()
    erro = models.FloatField()

    def clean(self):
        if not (0 <= self.acerto <= 1):
            raise ValidationError({'acerto': 'O valor de acerto deve estar entre 0 e 1.'})
        if not (0 <= self.erro <= 1):
            raise ValidationError({'erro': 'O valor de erro deve estar entre 0 e 1.'})

    def __str__(self):
        return f"{self.serie} - {self.habilidade}"

############################################################################################################################
class Aluno(models.Model):
    # Campos para o modelo Aluno
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField(null=True, blank=True)  # Exemplo de outro campo que você pode precisar
    matricula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    serie = models.IntegerField(null=True, blank=True)  # Relacionando com a série

    def __str__(self):
        return self.nome
############################################################################################################################

class Professor(models.Model):
    # Campos para o modelo Professor
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)  # CPF com campo único
    email = models.EmailField(null=True, blank=True)
    especialidade = models.CharField(max_length=100, null=True, blank=True)  # Exemplo de especialidade

    def __str__(self):
        return self.nome
############################################################################################################################

class HabilidadePortugues(models.Model):
    # Campos para habilidades de Português
    habilidade = models.CharField(max_length=100)
    topico = models.CharField(max_length=100)  # Campo para o tópico da habilidade
    descricao = models.TextField()
    serie = models.IntegerField()  # Série correspondente à habilidade
    tipo_ano = models.CharField(
        max_length=10,
        choices=[('inicial', 'Anos Iniciais'), ('final', 'Anos Finais')],
        default='inicial'
    )
    acertos = models.FloatField(default=0.0)  # Percentual de acertos
    erros = models.FloatField(default=0.0)    # Percentual de erros

    def __str__(self):
        return f"{self.habilidade} - {self.descricao[:30]}"  # Retorno amigável no admin
############################################################################################################################

class HabilidadeMatematica(models.Model):
    # Campos para habilidades de Matemática
    habilidade = models.CharField(max_length=100)
    topico = models.CharField(max_length=100)  # Campo para o tópico da habilidade
    descricao = models.TextField()
    serie = models.IntegerField()  # Série correspondente à habilidade
    tipo_ano = models.CharField(
        max_length=10,
        choices=[('inicial', 'Anos Iniciais'), ('final', 'Anos Finais')],
        default='inicial'
    )
    acertos = models.FloatField(default=0.0)  # Percentual de acertos
    erros = models.FloatField(default=0.0)    # Percentual de erros

    def __str__(self):
        return f"{self.habilidade} - {self.descricao[:30]}"  # Retorno amigável no admin
############################################################################################################################
class Suporte(models.Model):
    assunto = models.CharField(max_length=100)
    descricao = models.TextField()
    urgencia = models.CharField(max_length=10)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assunto} - {self.urgencia}"
############################################################################################################################

class Feedback(models.Model):
    comentario = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback em {self.data_criacao}"
############################################################################################################################
from django.db import models

class ExameSuplencia(models.Model):
    ano_exame = models.IntegerField()
    numero = models.CharField(max_length=50)
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14)
    portugues = models.FloatField()
    redacao = models.FloatField()
    media_ling = models.FloatField(blank=True, null=True)
    ingles = models.FloatField()
    arte = models.FloatField()
    ed_fisica = models.FloatField()
    historia = models.FloatField()
    geografia = models.FloatField()
    matematica = models.FloatField()
    ciencias = models.FloatField()
    observacao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    materias_aprovadas = models.JSONField(blank=True, null=True)

    def calcular_media_e_status(self):
        self.media_ling = (self.portugues + self.redacao) / 2
        self.status = "Aprovado" if self.media_ling >= 7 else "Reprovado"
        self.materias_aprovadas = [
            materia for materia, nota in {
                "Inglês": self.ingles,
                "Arte": self.arte,
                "Educação Física": self.ed_fisica,
                "História": self.historia,
                "Geografia": self.geografia,
                "Matemática": self.matematica,
                "Ciências": self.ciencias
            }.items() if nota >= 7
        ]
############################################################################################################################
from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class Registro(models.Model):
    ano_exame = models.IntegerField(null=True, blank=True)
    numero = models.CharField(max_length=10, unique=True, null=False)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)

    portugues = models.FloatField(default=0)
    redacao = models.FloatField(default=0)
    media_ling = models.FloatField(default=0)
    ingles = models.FloatField(default=0)
    arte = models.FloatField(default=0)
    ed_fisica = models.FloatField(default=0)
    historia = models.FloatField(default=0)
    geografia = models.FloatField(default=0)
    matematica = models.FloatField(default=0)
    ciencias = models.FloatField(default=0)

    observacao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20)
    materias_aprovadas = models.TextField(blank=True, null=True)

    certificado_emitido = models.BooleanField(default=False)
    certificado_data_emissao = models.DateField(null=True, blank=True)
    certificado_numero = models.CharField(max_length=50, blank=True, null=True)

    atestado_emitido = models.BooleanField(default=False)
    atestado_data_emissao = models.DateField(null=True, blank=True)
    atestado_numero = models.CharField(max_length=50, blank=True, null=True)

    email = models.EmailField()
    data_nascimento = models.DateField(null=True, blank=True)
    maior_de_18 = models.BooleanField(default=True)

    nome_responsavel = models.CharField(max_length=255, blank=True, null=True)
    cpf_responsavel = models.CharField(max_length=14, blank=True, null=True)
    rg_responsavel = models.CharField(max_length=20, blank=True, null=True)
    tipo_responsavel = models.CharField(max_length=20, blank=True, null=True)

    telefone = models.CharField(max_length=20)
    telefone_2 = models.CharField(max_length=20, blank=True, null=True)
    cidade = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    bairro = models.ForeignKey('Bairro', on_delete=models.SET_NULL, null=True, blank=True)

    fez_exame_supletivo = models.CharField(max_length=3)
    ano_ultima_prova = models.IntegerField(blank=True, null=True)
    prova_todas_disciplinas = models.CharField(max_length=3)
    disciplinas = models.TextField(blank=True, null=True)

    possui_necessidade_especial = models.CharField(max_length=3)
    necessidade_especial_detalhe = models.CharField(max_length=100, blank=True, null=True)

    senha = models.CharField(max_length=128)
    local_prova = models.CharField(max_length=255)
    escola_2024 = models.CharField(max_length=255)
    termos_condicoes = models.BooleanField(default=False)

    data_inscricao = models.DateTimeField(auto_now_add=True)
    token_recuperacao = models.UUIDField(null=True, blank=True)
    token_expira_em = models.DateTimeField(null=True, blank=True)

    reinscricao = models.BooleanField(default=False)
    reinscrito = models.BooleanField(default=False)
    data_prova = models.DateField(null=True, blank=True)

    # Campos novos
    deseja_participar_aulao = models.CharField(
        max_length=3,
        choices=[("Sim", "Sim"), ("Não", "Não")],
        default="Não"
    )
    turnos_aulao = models.TextField(
        blank=True, null=True,
        help_text="Turnos selecionados: Matutino, Vespertino, Noturno"
    )

    def token_esta_valido(self):
        return self.token_expira_em and self.token_expira_em > timezone.now()

    def set_senha(self, raw_password):
        self.senha = make_password(raw_password)
        self.save(update_fields=["senha"])

    def check_senha(self, raw_password):
        return check_password(raw_password, self.senha)

    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"


############################################################################################################################


from django.db import models

class DiagnoseInicProfMat(models.Model):
    item = models.CharField(max_length=50)
    habilidade = models.TextField()
    descricao_habilidade = models.TextField()
    etapa_aplicacao = models.CharField(max_length=10)

    def __str__(self):
        return self.item




from django.db import models
from django.conf import settings


class Candidato(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidato')
    nome_completo = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    email = models.EmailField()
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cidade = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    fez_exame_supletivo = models.BooleanField(default=False)
    disciplinas = models.TextField(blank=True, null=True)
    possui_necessidade_especial = models.BooleanField(default=False)
    necessidade_especial_detalhe = models.CharField(max_length=100, blank=True, null=True)
    
    local_prova = models.CharField(max_length=100)
    data_prova = models.DateField()
    escola_2024 = models.CharField(max_length=100)
    
    status = models.CharField(max_length=30, default='Inscrição recebida')  # ou: aprovado, pendente...

    data_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo


# webapp/models.py
from django.db import models

class Bairro(models.Model):
    bairro_distrito = models.CharField(max_length=100)
    cep = models.CharField(max_length=20)
    logradouro_nome = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.bairro_distrito} ({self.cep})"


# models.py

from django.db import models

class Disciplina(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    etapa = models.CharField(max_length=50, blank=True, null=True)  # Ex: Ensino Fundamental, Médio
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome



def pode_reinscrever(self):
    return (
        self.ano_exame == 2025 and
        self.reinscricao is False and
        Registro.objects.filter(cpf=self.cpf, ano_exame=2024).exists()
    )


# models.py

class Escola(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
