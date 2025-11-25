from mvc.models.pagamentos_model import PagamentoModel
from dao import PagamentosDAO
from datetime import date
from mvc.models.forma_pagamento_enum import FormaPagamento
from typing import List, Optional

class PagamentosController:
    """Controlador para gerenciar operações relacionadas a pagamentos."""

    def __init__(self, user_id=None):
        self.dao = PagamentosDAO(user_id=user_id)

    def criar_pagamento(self, nome: str, vencimento: Optional[date], forma_pagamento: FormaPagamento) -> int:
        """
        Cria um novo pagamento.
        
        Args:
            nome: Nome do pagamento
            vencimento: Data de vencimento
            forma_pagamento: Forma de pagamento (enum FormaPagamento)
            
        Returns:
            ID do pagamento criado
        """
        pagamento = PagamentoModel(nome, vencimento, forma_pagamento)
        return self.dao.add_pagamento(pagamento)

    def listar_pagamentos(self) -> List[PagamentoModel]:
        """
        Lista todos os pagamentos cadastrados.
        
        Returns:
            Lista de objetos PagamentoModel
        """
        return self.dao.get_all_pagamentos()

    def atualizar_pagamento(self, pagamento_id: int, nome: str, vencimento: Optional[date], 
                          forma_pagamento: FormaPagamento) -> None:
        """
        Atualiza um pagamento existente.
        
        Args:
            pagamento_id: ID do pagamento a ser atualizado
            nome: Novo nome
            vencimento: Nova data de vencimento
            forma_pagamento: Nova forma de pagamento
        """
        pagamento = PagamentoModel(nome, vencimento, forma_pagamento)
        self.dao.update_pagamento(pagamento_id, pagamento)

    def excluir_pagamento(self, pagamento_id: int) -> None:
        """
        Exclui um pagamento.
        
        Args:
            pagamento_id: ID do pagamento a ser excluído
        """
        self.dao.delete_pagamento(pagamento_id)
        
    def obter_nomes_metodos_pagamento(self) -> List[str]:
        """
        Retorna uma lista com os nomes dos métodos de pagamento cadastrados.
        
        Returns:
            Lista de strings com os nomes dos métodos de pagamento
        """
        pagamentos = self.dao.get_all_pagamentos()
        return [p.nome for p in pagamentos]