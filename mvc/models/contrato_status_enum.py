from enum import Enum

class StatusContrato(Enum):
    """Enum que define os status possíveis de um contrato."""
    ATIVO = "Ativo"
    CANCELADO = "Cancelado"
    ENCERRADO = "Encerrado"