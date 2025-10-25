from enum import Enum

class FormaPagamento(Enum):
    """Enum que define as formas de pagamento disponíveis."""
    DINHEIRO = "Dinheiro"
    CARTAO_CREDITO = "Cartão de crédito"
    CARTAO_DEBITO = "Cartão de débito"
    PIX = "PIX"
    GIFT_CARD = "Gift card"
    OUTROS = "Outros"