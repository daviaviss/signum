from mvc.models.contratos_model import Contrato
from mvc.models.assinatura_status_enum import StatusAssinatura
from datetime import datetime


class Assinatura(Contrato):
    """Model para Assinatura - herda de Contrato e adiciona login/senha e forma de pagamento."""
    
    def __init__(
        self, 
        nome: str, 
        data_vencimento: str, 
        valor: float, 
        periodicidade: str,
        tag: str,
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
        # Se tag vier como enum, usa seu value
        tag_value = getattr(tag, "value", tag)
        super().__init__(
            nome=nome,
            valor=valor,
            data_vencimento=data_vencimento,
            periodicidade=periodicidade,
            tag=tag_value,
            usuario_compartilhado=usuario_compartilhado,
            favorito=favorito,
            contrato_id=assinatura_id,
            user_id=user_id
        )
        self.forma_pagamento = forma_pagamento
        self.login = login
        self.senha = senha
        self.created_at = created_at if created_at else datetime.now().isoformat()
        self.is_readonly = False  # Por padrão, não é readonly (será setado pelo DAO)
        
        # Define status
        if status is None:
            self.status = StatusAssinatura.ATIVO
        elif isinstance(status, StatusAssinatura):
            self.status = status
        elif isinstance(status, str):
            self.status = StatusAssinatura(status)
        else:
            self.status = StatusAssinatura.ATIVO
    
    @property
    def tipo(self) -> str:
        return "assinatura"
    
    def __repr__(self):
        return f"<Assinatura id={self.id} nome={self.nome} valor={self.valor}>"


# Removido: classe AssinaturasModel. Controllers agora usam DAO e enums diretamente.
