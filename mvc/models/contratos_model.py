from abc import ABC, abstractmethod
from mvc.models.contrato_status_enum import StatusContrato

class Contrato(ABC):
    """Classe base abstrata para Contrato."""
    def __init__(
        self,
        nome: str,
        valor: float,
        data_vencimento: str,
        periodicidade: str,
        tag: str,
        usuario_compartilhado: str = "",
        favorito: int = 0,
        contrato_id: int = None,
        user_id: int = None,
        status: StatusContrato = StatusContrato.ATIVO,
    ):
        self.id = contrato_id
        self.user_id = user_id
        self.nome = nome
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.periodicidade = periodicidade
        self.tag = tag
        self.usuario_compartilhado = usuario_compartilhado
        self.favorito = favorito
        self.status = status

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Tipo do contrato (e.g., 'contrato', 'assinatura')."""
        raise NotImplementedError

    def __repr__(self):
        return f"<Contrato id={self.id} nome={self.nome} valor={self.valor}>"


class ContratoGenerico(Contrato):
    """Contrato genérico concreto (sem pagamento/login/senha)."""
    @property
    def tipo(self) -> str:
        return "contrato"
    
