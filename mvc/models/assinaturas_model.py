from mvc.models.contratos_model import Contrato


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
        user_id: int = None
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
    
    @property
    def tipo(self) -> str:
        return "assinatura"
    
    def __repr__(self):
        return f"<Assinatura id={self.id} nome={self.nome} valor={self.valor}>"


# Removido: classe AssinaturasModel. Controllers agora usam DAO e enums diretamente.
