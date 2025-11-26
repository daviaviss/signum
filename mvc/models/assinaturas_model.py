from mvc.models.contratos_model import Contrato
from mvc.models.status_enum import Status
from datetime import datetime


class Assinatura(Contrato):
    """Model para Assinatura - herda de Contrato e adiciona login/senha e forma de pagamento."""
    
    def __init__(
        self, 
        nome: str, 
        data_vencimento: str, 
        valor: float, 
        periodicidade: str,
        categoria: str,
        forma_pagamento: str,
        usuario_compartilhado: str = "",
        login: str = "",
        senha: str = "",
        favorito: int = 0,
        assinatura_id: int = None,
        user_id: int = None,
        status = None,
        created_at: str = None
    ):
        # Se categoria vier como enum, usa seu value (necessário para compatibilidade)
        categoria_value = getattr(categoria, "value", categoria)
        super().__init__(
            nome=nome,
            valor=valor,
            data_vencimento=data_vencimento,
            periodicidade=periodicidade,
            categoria=categoria_value,
            forma_pagamento=forma_pagamento,
            usuario_compartilhado=usuario_compartilhado,
            favorito=favorito,
            contrato_id=assinatura_id,
            user_id=user_id
        )
        self.login = login
        self.senha = senha
        self.created_at = created_at if created_at else datetime.now().isoformat()
        self.is_readonly = False
        
        # status: define o estado da assinatura
        if status is None:
            self.status = Status.ATIVO
        elif isinstance(status, Status):
            self.status = status
        elif isinstance(status, str):
            self.status = Status(status)
        else:
            self.status = Status.ATIVO
    
    @property
    def tipo(self) -> str:
        return "assinatura"
    
    def __repr__(self):
        return f"<Assinatura id={self.id} nome={self.nome} valor={self.valor}>"



