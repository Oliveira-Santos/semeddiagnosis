import random
import string

def gerar_numero_unico():
    # Exemplo: gera um código como "CAND-2025-XYZ123"
    return 'CAND-2025-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
