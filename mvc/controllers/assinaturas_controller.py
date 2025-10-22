from mvc.models.assinaturas_model import AssinaturasModel
from dao import AssinaturasDAO


class AssinaturasController:
    """Controller para Assinaturas."""
    
    def __init__(self, view, user_id=None):
        self.view = view
        self.user_id = user_id
        self.dao = AssinaturasDAO()
        self.model = AssinaturasModel(dao=self.dao)
        self.view.controller = self
        
        # Popula os comboboxes
        self.view.set_combo_values(
            self.model.PERIODICIDADES,
            self.model.TAGS_DISPONIVEIS,
            self.model.FORMAS_PAGAMENTO
        )
        
        self._carregar_assinaturas()
    
    def _carregar_assinaturas(self):
        """Carrega e exibe as assinaturas do usuário."""
        if self.user_id:
            assinaturas = self.model.listar_assinaturas(self.user_id)
            self.view.atualizar_lista(assinaturas)
    
    def adicionar(
        self,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        tag: str,
        forma_pagamento: str,
        usuario_compartilhado: str = "",
        login: str = "",
        senha: str = ""
    ):
        """Adiciona uma nova assinatura."""
        if not self.user_id:
            return False
        
        self.model.adicionar_assinatura(
            user_id=self.user_id,
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            tag=tag,
            forma_pagamento=forma_pagamento,
            usuario_compartilhado=usuario_compartilhado,
            login=login,
            senha=senha
        )
        self._carregar_assinaturas()
        return True
    
    def remover(self, assinatura_id: int):
        """Remove uma assinatura."""
        self.model.remover_assinatura(assinatura_id)
        self._carregar_assinaturas()
    
    def toggle_favorito(self, assinatura_id: int):
        """Alterna o status de favorito de uma assinatura."""
        if self.user_id:
            self.model.toggle_favorito(assinatura_id, self.user_id)
            self._carregar_assinaturas()
    
    def get_tags_disponiveis(self):
        """Retorna lista de tags disponíveis."""
        return AssinaturasModel.TAGS_DISPONIVEIS
    
    def get_periodicidades(self):
        """Retorna lista de periodicidades disponíveis."""
        return AssinaturasModel.PERIODICIDADES
    
    def get_formas_pagamento(self):
        """Retorna lista de formas de pagamento disponíveis."""
        return AssinaturasModel.FORMAS_PAGAMENTO
