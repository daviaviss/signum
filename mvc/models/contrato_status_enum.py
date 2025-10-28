from enum import Enum

class StatusContrato(Enum):
    """Enum que define os status possíveis de um contrato."""
    ATIVO = "Ativo"
    PAUSADO = "Pausado"
    ENCERRADO = "Encerrado"