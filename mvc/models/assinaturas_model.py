class Assinatura:
    """Model para Assinatura."""
    
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
        self.id = assinatura_id
        self.user_id = user_id
        self.nome = nome
        self.data_vencimento = data_vencimento
        self.valor = valor
        self.periodicidade = periodicidade  # Mensal, Trimestral, Semestral, Anual
        self.tag = tag  # Streaming, Software, Educação, etc.
        self.forma_pagamento = forma_pagamento  # Cartão de Crédito, Débito, PIX, Boleto
        self.usuario_compartilhado = usuario_compartilhado
        self.login = login
        self.senha = senha
        self.favorito = favorito  # 0 = não favorito, 1 = favorito
    
    def __repr__(self):
        return f"<Assinatura id={self.id} nome={self.nome} valor={self.valor}>"


class AssinaturasModel:
    """Model que gerencia assinaturas."""
    
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
    
    # Formas de pagamento
    FORMAS_PAGAMENTO = [
        "Cartão de Crédito",
        "Cartão de Débito",
        "PIX",
        "Boleto",
        "Transferência Bancária"
    ]
    
    def __init__(self, dao=None):
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
