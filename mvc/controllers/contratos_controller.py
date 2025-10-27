from dao import ContratosDAO
from mvc.models.contratos_model import Contrato
from mvc.models.periodicidade_enum import Periodicidade
from mvc.models.contrato_categoria_enum import CategoriaContrato
from mvc.models.contrato_status_enum import StatusContrato


class ContratosController:
    """Controller para Contratos (genérico, sem pagamento/login/senha)."""
    
    def __init__(self, view, user_id=None):
        self.view = view
        self.user_id = user_id
        self.dao = ContratosDAO()
        # Removido ContratosModel; controller usa DAO diretamente
        self.view.controller = self
        
        # Popula os comboboxes (periodicidade e tags) via enums
        self.view.set_combo_values(
            [p.value for p in Periodicidade],
            [c.value for c in CategoriaContrato],
        )
        
        self._carregar_contratos()
    
    def _carregar_contratos(self):
        """Carrega e exibe os contratos do usuário."""
        if self.user_id:
            rows = self.dao.get_contratos_by_user(self.user_id)
            contratos = [
                Contrato(
                    contrato_id=r["id"],
                    user_id=r["user_id"],
                    nome=r["nome"],
                    data_vencimento=r["data_vencimento"],
                    valor=r["valor"],
                    periodicidade=r["periodicidade"],
                    tag=r["tag"],
                    usuario_compartilhado=r.get("usuario_compartilhado") or "",
                    favorito=1 if r.get("favorito") else 0,
                    status=StatusContrato(r.get("status", StatusContrato.ATIVO.value))
                )
                for r in rows
            ]
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
        
        contrato = Contrato(
            nome=nome,
            valor=valor,
            data_vencimento=data_vencimento,
            periodicidade=periodicidade,
            tag=tag,
            usuario_compartilhado=usuario_compartilhado,
            favorito=0,
            user_id=self.user_id,
            status=StatusContrato.ATIVO,
        )
        self.dao.add_contrato(contrato)
        self._carregar_contratos()
        return True
    
    def remover(self, contrato_id: int):
        """Remove um contrato."""
        self.dao.delete_contrato(contrato_id)
        self._carregar_contratos()
    
    def toggle_favorito(self, contrato_id: int):
        """Alterna o status de favorito de um contrato."""
        if self.user_id:
            self.dao.toggle_favorito(contrato_id)
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
        
        contrato = Contrato(
            nome=nome,
            valor=valor,
            data_vencimento=data_vencimento,
            periodicidade=periodicidade,
            tag=tag,
            usuario_compartilhado=usuario_compartilhado,
            favorito=favorito,
            contrato_id=contrato_id,
            user_id=self.user_id,
            status=StatusContrato.ATIVO,
        )
        self.dao.update_contrato(contrato)
        self._carregar_contratos()
        return True
    
    def get_tags_disponiveis(self):
        """Retorna lista de tags disponíveis."""
        return [c.value for c in CategoriaContrato]
    
    def get_periodicidades(self):
        """Retorna lista de periodicidades disponíveis."""
        return [p.value for p in Periodicidade]