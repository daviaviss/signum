from enum import Enum

class CategoriaAssinatura(Enum):
    """Enum que define categorias de assinatura."""
    STREAMING = "Streaming"
    CLUBES = "Clubes"
    ALIMENTACAO = "Alimentação"
    SAAS = "SaaS"
    PETS = "Pets"
    OUTROS = "Outros"