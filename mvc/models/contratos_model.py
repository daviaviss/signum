class Contrato:
    """Model para Contrato."""
    
    def __init__(self, nome: str, valor: float, data: str, contrato_id: int = None):
        self.id = contrato_id
        self.nome = nome
        self.valor = valor
        self.data = data
    
    def __repr__(self):
        return f"<Contrato id={self.id} nome={self.nome} valor={self.valor}>"


class ContratosModel:
    """Model que gerencia contratos."""
    
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
