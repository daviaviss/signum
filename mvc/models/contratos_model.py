class Contrato:
    """Model para Contrato."""
    
    def __init__(
        self, 
        nome: str, 
        valor: float, 
        data_vencimento: str,
        periodicidade: str,
        tag: str,
        forma_pagamento: str,
        usuario_compartilhado: str = "",
        favorito: int = 0,
        contrato_id: int = None,
        user_id: int = None
    ):
        self.id = contrato_id
        self.user_id = user_id
        self.nome = nome
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.periodicidade = periodicidade  # Mensal, Trimestral, Semestral, Anual
        self.tag = tag  # Streaming, Software, Educação, etc.
        self.forma_pagamento = forma_pagamento  # Cartão de Crédito, Débito, PIX, Boleto
        self.usuario_compartilhado = usuario_compartilhado
        self.favorito = favorito  # 0 = não favorito, 1 = favorito
    
    def __repr__(self):
        return f"<Contrato id={self.id} nome={self.nome} valor={self.valor}>"


class ContratosModel:
    """Model que gerencia contratos."""
    
    # Tags pré-definidas
    TAGS_DISPONIVEIS = [
        "Streaming",
        "Software",
        "Educação",
        "Saúde",
        "Fitness",
        "Entretenimento",
        "Produtividade",
        "Outro"
    ]
    
    # Periodicidades disponíveis
    PERIODICIDADES = [
        "Mensal",
        "Trimestral",
        "Semestral",
        "Anual"
    ]
    
    
    
    def __init__(self):
        # Temporário: lista em memória (futuramente usar DAO)
        self.contratos = []
    
    def adicionar_contrato(self, nome: str, valor: float, data: str):
        contrato = Contrato(nome, valor, data, len(self.contratos) + 1)
        self.contratos.append(contrato)
        return True
    
    def listar_contratos(self):
        return self.contratos
    
    def remover_contrato(self, contrato_id: int):
        self.contratos = [c for c in self.contratos if c.id != contrato_id]
