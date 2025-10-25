from datetime import date
from typing import Optional
from mvc.models.forma_pagamento_enum import FormaPagamento

class PagamentoModel:
    """Modelo para representar informações de pagamento."""
    
    def __init__(self, nome: str, vencimento: date, forma_de_pagamento: FormaPagamento):
        self.nome = nome
        self.vencimento = vencimento
        self.forma_de_pagamento = forma_de_pagamento
    
    @property
    def nome(self) -> str:
        """Nome associado ao pagamento."""
        return self._nome

    @nome.setter
    def nome(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Nome deve ser uma string")
        if not value.strip():
            raise ValueError("Nome não pode ser vazio")
        # Limpa espaços e capitaliza a primeira letra
        nome_limpo = value.strip()
        self._nome = nome_limpo[0].upper() + nome_limpo[1:] if nome_limpo else nome_limpo

    @property
    def vencimento(self) -> date:
        """Data de vencimento do pagamento."""
        return self._vencimento

    @vencimento.setter
    def vencimento(self, value: Optional[date]):
        if value is not None and not isinstance(value, date):
            raise TypeError("Vencimento deve ser um objeto date ou None")
        self._vencimento = value

    @property
    def forma_de_pagamento(self) -> FormaPagamento:
        """Forma de pagamento selecionada."""
        return self._forma_de_pagamento

    @forma_de_pagamento.setter
    def forma_de_pagamento(self, value: FormaPagamento):
        if not isinstance(value, FormaPagamento):
            raise TypeError("Forma de pagamento deve ser um FormaPagamento")
        self._forma_de_pagamento = value