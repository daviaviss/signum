from dao import AssinaturasDAO
from mvc.models.assinaturas_model import Assinatura
from mvc.models.periodicidade_enum import Periodicidade
from mvc.models.assinatura_categoria_enum import CategoriaAssinatura


class AssinaturasController:
    """Controller para Assinaturas."""
    
    def __init__(self, view, user_id=None):
        self.view = view
        self.user_id = user_id
        self.dao = AssinaturasDAO()
        # Removido AssinaturasModel; controller usa DAO diretamente
        self.view.controller = self
        
        # Importa o controller de pagamentos para obter os métodos cadastrados
        from mvc.controllers.pagamentos_controller import PagamentosController
        self.pagamentos_controller = PagamentosController()
        
        # Popula os comboboxes usando enums diretamente
        self.view.set_combo_values(
            [p.value for p in Periodicidade],
            [c.value for c in CategoriaAssinatura],
            self.pagamentos_controller.obter_nomes_metodos_pagamento()
        )
        
        self._carregar_assinaturas()
    
    def _carregar_assinaturas(self):
        """Carrega e exibe as assinaturas do usuário."""
        if self.user_id:
            assinaturas = self.dao.get_assinaturas_by_user(self.user_id)
            self.view.atualizar_lista(assinaturas)
    
    def adicionar(
        self,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        categoria: str,
        forma_pagamento: str,
        usuario_compartilhado: str = "",
        login: str = "",
        senha: str = ""
    ):
        """Adiciona uma nova assinatura."""
        if not self.user_id:
            return False
        
        assinatura = Assinatura(
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            tag=categoria,  # Map categoria back to tag for model compatibility
            forma_pagamento=forma_pagamento,
            usuario_compartilhado=usuario_compartilhado,
            login=login,
            senha=senha,
            favorito=0,
            user_id=self.user_id
        )
        self.dao.add_assinatura(assinatura)
        self._carregar_assinaturas()
        return True
    
    def remover(self, assinatura_id: int):
        """Remove uma assinatura."""
        self.dao.delete_assinatura(assinatura_id)
        self._carregar_assinaturas()
    
    def toggle_favorito(self, assinatura_id: int):
        """Alterna o status de favorito de uma assinatura."""
        if self.user_id:
            self.dao.toggle_favorito(assinatura_id)
            self._carregar_assinaturas()
    
    def editar(
        self,
        assinatura_id: int,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        categoria: str,
        forma_pagamento: str,
        usuario_compartilhado: str = "",
        login: str = "",
        senha: str = "",
        favorito: int = 0
    ):
        """Edita uma assinatura existente."""
        if not self.user_id:
            return False
        
        assinatura = Assinatura(
            assinatura_id=assinatura_id,
            user_id=self.user_id,
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            tag=categoria,  # Map categoria back to tag for model compatibility
            forma_pagamento=forma_pagamento,
            usuario_compartilhado=usuario_compartilhado,
            login=login,
            senha=senha,
            favorito=favorito
        )
        self.dao.update_assinatura(assinatura)
        self._carregar_assinaturas()
        return True
    
    def get_categorias_disponiveis(self):
        """Retorna lista de categorias disponíveis."""
        return [c.value for c in CategoriaAssinatura]
    
    def get_periodicidades(self):
        """Retorna lista de periodicidades disponíveis."""
        return [p.value for p in Periodicidade]
    
    def get_formas_pagamento(self):
        """Retorna lista de formas de pagamento cadastradas."""
        return self.pagamentos_controller.obter_nomes_metodos_pagamento()
