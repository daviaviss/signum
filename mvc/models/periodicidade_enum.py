from enum import Enum

class Periodicidade(Enum):
    """Enum para periodicidades de contratos e assinaturas."""
    MENSAL = "Mensal"
    TRIMESTRAL = "Trimestral"
    SEMESTRAL = "Semestral"
    ANUAL = "Anual"