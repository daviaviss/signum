from mvc.models.contratos_model import ContratosModel


class ContratosController:
    """Controller para Contratos."""
    
    def __init__(self, view):
        self.view = view
        self.model = ContratosModel()
        self.view.controller = self
        self._carregar_contratos()
    
    def _carregar_contratos(self):
        """Carrega e exibe os contratos."""
        contratos = self.model.listar_contratos()
        self.view.atualizar_lista(contratos)
    
    def adicionar(self, nome: str, valor: float, data: str):
        """Adiciona um novo contrato."""
        self.model.adicionar_contrato(nome, valor, data)
        self._carregar_contratos()
    
    def remover(self, contrato_id: int):
        """Remove um contrato."""
        self.model.remover_contrato(contrato_id)
        self._carregar_contratos()
