from mvc.models.contratos_model import ContratosModel
from dao import ContratosDAO


class ContratosController:
    """Controller para Contratos (genérico, sem pagamento/login/senha)."""
    
    def __init__(self, view, user_id=None):
        self.view = view
        self.user_id = user_id
        self.dao = ContratosDAO()
        self.model = ContratosModel(dao=self.dao)
        self.view.controller = self
        
        # Popula os comboboxes (periodicidade e tags)
        self.view.set_combo_values(
            self.model.PERIODICIDADES,
            self.model.TAGS_DISPONIVEIS,
        )
        
        self._carregar_contratos()
    
    def _carregar_contratos(self):
        """Carrega e exibe os contratos do usuário."""
        if self.user_id:
            contratos = self.model.listar_contratos(self.user_id)
            self.view.atualizar_lista(contratos)
    
    def adicionar(
        self,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        tag: str,
        usuario_compartilhado: str = "",
    ):
        """Adiciona um novo contrato."""
        if not self.user_id:
            return False
        
        self.model.adicionar_contrato(
            user_id=self.user_id,
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            tag=tag,
            usuario_compartilhado=usuario_compartilhado,
        )
        self._carregar_contratos()
        return True
    
    def remover(self, contrato_id: int):
        """Remove um contrato."""
        self.model.remover_contrato(contrato_id)
        self._carregar_contratos()
    
    def toggle_favorito(self, contrato_id: int):
        """Alterna o status de favorito de um contrato."""
        if self.user_id:
            self.model.toggle_favorito(contrato_id, self.user_id)
            self._carregar_contratos()
    
    def editar(
        self,
        contrato_id: int,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        tag: str,
        usuario_compartilhado: str = "",
        favorito: int = 0,
    ):
        """Edita um contrato existente."""
        if not self.user_id:
            return False
        
        self.model.editar_contrato(
            contrato_id=contrato_id,
            user_id=self.user_id,
            nome=nome,
            data_vencimento=data_vencimento,
            valor=valor,
            periodicidade=periodicidade,
            tag=tag,
            usuario_compartilhado=usuario_compartilhado,
            favorito=favorito,
        )
        self._carregar_contratos()
        return True
    
    def get_tags_disponiveis(self):
        """Retorna lista de tags disponíveis."""
        return ContratosModel.TAGS_DISPONIVEIS
    
    def get_periodicidades(self):
        """Retorna lista de periodicidades disponíveis."""
        return ContratosModel.PERIODICIDADES