import pandas as pd
from .models import Registro
import csv

def processar_planilha(file_path):
    """
    Função para processar uma planilha Excel e salvar os dados no banco de dados.

    Args:
        file_path (str): Caminho do arquivo Excel.
    """
    try:
        # Carregar a planilha
        df = pd.read_excel(file_path)

        # Iterar sobre as linhas da planilha e salvar os dados no banco de dados
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
                materias_aprovadas=row.get('MATERIAS APROVADAS', None),
            )
    except Exception as e:
        print(f"Erro ao processar a planilha: {e}")
        raise


def processar_csv_e_salvar_no_banco(caminho_csv):
    with open(caminho_csv, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        registros = []
        for row in reader:
            registro = Registro(
                ano_exame=row.get("ANO DO EXAME DE SUPLENCIA"),
                numero=row.get("NÚMERO"),
                nome=row.get("NOME"),
                cpf=row.get("CPF"),
                portugues=float(row.get("PORTUGUÊS", 0)),
                redacao=float(row.get("REDAÇÃO", 0)),
                media_ling=(float(row.get("PORTUGUÊS", 0)) + float(row.get("REDAÇÃO", 0))) / 2,
                ingles=float(row.get("INGLÊS", 0)),
                arte=float(row.get("ARTE", 0)),
                ed_fisica=float(row.get("ED. FÍSICA", 0)),
                historia=float(row.get("HISTÓRIA", 0)),
                geografia=float(row.get("GEOGRAFIA", 0)),
                matematica=float(row.get("MATEMÁTICA", 0)),
                ciencias=float(row.get("CIÊNCIAS", 0)),
                observacao=row.get("OBSERVAÇÃO", ""),
                status=row.get("STATUS"),
                materias_aprovadas=row.get("MATERIAS APROVADAS", "")
            )
            registros.append(registro)
        Registro.objects.bulk_create(registros)