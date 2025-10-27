from enum import Enum

class CategoriaContrato(Enum):
    """Enum para categorias de contratos."""
    SERVICOS_PROFISSIONAIS = "Serviços profissionais"
    EDUCACAO = "Educação"
    FINANCIAMENTO = "Financiamento"
    SAUDE = "Saude"
    ALUGUEL = "Aluguel"
    OUTROS = "Outros"