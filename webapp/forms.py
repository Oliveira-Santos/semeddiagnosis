from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Importar o modelo de usuário personalizado
from .models import Suporte, Feedback
from .models import Registro  # Certifique-se de importar o modelo correto


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Select a CSV file")

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Especificar o modelo CustomUser
        fields = ('username', 'email', 'password1', 'password2')  # Campos que você deseja no formulário
############################################################################################################################
class SuporteForm(forms.ModelForm):
    class Meta:
        model = Suporte
        fields = ['assunto', 'descricao', 'urgencia']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'urgencia': forms.Select(choices=[('Baixa', 'Baixa'), ('Média', 'Média'), ('Alta', 'Alta')])
        }
############################################################################################################################

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }
############################################################################################################################
from django import forms

class UploadFileForm(forms.Form):
    arquivo = forms.FileField()
############################################################################################################################
class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro  # Aqui é onde o erro ocorreu. Certifique-se de que 'Registro' está importado.
        fields = ['nome', 'cpf', 'status', 'observacao']