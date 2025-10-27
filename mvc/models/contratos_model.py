from mvc.models.contrato_status_enum import StatusContrato

class Contrato:
    """Classe concreta para Contrato (sem pagamento/login/senha)."""
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
    def tipo(self) -> str:
        """Tipo do registro; por padrão, 'contrato'."""
        return "contrato"

    def __repr__(self):
        return f"<Contrato id={self.id} nome={self.nome} valor={self.valor}>"
    
