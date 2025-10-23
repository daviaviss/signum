from mvc.models.contratos_model import Contrato, ContratosModel


class Assinatura(Contrato):
    """Model para Assinatura - herda de Contrato e adiciona login/senha."""
    
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
        super().__init__(
            nome=nome,
            valor=valor,
            data_vencimento=data_vencimento,
            periodicidade=periodicidade,
            tag=tag,
            forma_pagamento=forma_pagamento,
            usuario_compartilhado=usuario_compartilhado,
            favorito=favorito,
            contrato_id=assinatura_id,
            user_id=user_id
        )
        self.login = login
        self.senha = senha
    
    def __repr__(self):
        return f"<Assinatura id={self.id} nome={self.nome} valor={self.valor}>"


class AssinaturasModel(ContratosModel):
    """Model que gerencia assinaturas - herda de ContratosModel."""
    
    def __init__(self, dao=None):
        super().__init__()
        self.dao = dao
    
    def adicionar_assinatura(
        self,
        user_id: int,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        tag: str,
        forma_pagamento: str,
        usuario_compartilhado: str = "",
        login: str = "",
        senha: str = "",
        favorito: int = 0
    ):
        assinatura = Assinatura(
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            tag=tag,
            forma_pagamento=forma_pagamento,
            usuario_compartilhado=usuario_compartilhado,
            login=login,
            senha=senha,
            favorito=favorito,
            user_id=user_id
        )
        if self.dao:
            self.dao.add_assinatura(assinatura)
        return True
    
    def listar_assinaturas(self, user_id: int):
        if self.dao:
            return self.dao.get_assinaturas_by_user(user_id)
        return []
    
    def remover_assinatura(self, assinatura_id: int):
        if self.dao:
            self.dao.delete_assinatura(assinatura_id)
    
    def toggle_favorito(self, assinatura_id: int, user_id: int):
        """Alterna o status de favorito de uma assinatura."""
        if self.dao:
            self.dao.toggle_favorito(assinatura_id)
    
    def editar_assinatura(
        self,
        assinatura_id: int,
        user_id: int,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        tag: str,
        forma_pagamento: str,
        usuario_compartilhado: str = "",
        login: str = "",
        senha: str = "",
        favorito: int = 0
    ):
        """Edita uma assinatura existente."""
        if self.dao:
            assinatura = Assinatura(
                assinatura_id=assinatura_id,
                user_id=user_id,
                nome=nome,
                data_vencimento=data_vencimento,
                valor=valor,
                periodicidade=periodicidade,
                tag=tag,
                forma_pagamento=forma_pagamento,
                usuario_compartilhado=usuario_compartilhado,
                login=login,
                senha=senha,
                favorito=favorito
            )
            self.dao.update_assinatura(assinatura)
        return True
    
    def obter_assinatura(self, assinatura_id: int):
        """Obtém uma assinatura específica por ID."""
        if self.dao:
            return self.dao.get_assinatura_by_id(assinatura_id)
        return None
