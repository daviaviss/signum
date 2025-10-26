from abc import ABC, abstractmethod

class Contrato(ABC):
    """Classe base abstrata para Contrato."""
    def __init__(
        self,
        nome: str,
        valor: float,
        data_vencimento: str,
        periodicidade: str,
        tag: str,
        usuario_compartilhado: str = "",
        favorito: int = 0,
        contrato_id: int = None,
        user_id: int = None,
    ):
        self.id = contrato_id
        self.user_id = user_id
        self.nome = nome
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.periodicidade = periodicidade
        self.tag = tag
        self.usuario_compartilhado = usuario_compartilhado
        self.favorito = favorito

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Tipo do contrato (e.g., 'contrato', 'assinatura')."""
        raise NotImplementedError

    def __repr__(self):
        return f"<Contrato id={self.id} nome={self.nome} valor={self.valor}>"


class ContratoGenerico(Contrato):
    """Contrato genérico concreto (sem pagamento/login/senha)."""
    @property
    def tipo(self) -> str:
        return "contrato"


class ContratosModel:
    """Model que gerencia contratos."""

    TAGS_DISPONIVEIS = [
        "Streaming",
        "Software",
        "Educação",
        "Saúde",
        "Fitness",
        "Entretenimento",
        "Produtividade",
        "Outro",
    ]

    PERIODICIDADES = [
        "Mensal",
        "Trimestral",
        "Semestral",
        "Anual",
    ]

    def __init__(self, dao=None):
        self.dao = dao
        self.contratos = []

    # -------- Persistência baseada em DAO --------
    def adicionar_contrato(
        self,
        user_id: int,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        tag: str,
        usuario_compartilhado: str = "",
        favorito: int = 0,
    ):
        contrato = ContratoGenerico(
            nome=nome,
            valor=valor,
            data_vencimento=data_vencimento,
            periodicidade=periodicidade,
            tag=tag,
            usuario_compartilhado=usuario_compartilhado,
            favorito=favorito,
            user_id=user_id,
        )
        if self.dao:
            self.dao.add_contrato(contrato)
            return True
        contrato.id = len(self.contratos) + 1
        self.contratos.append(contrato)
        return True

    def listar_contratos(self, user_id: int):
        if self.dao:
            rows = self.dao.get_contratos_by_user(user_id)
            # Converte dicts/rows em objetos
            return [
                ContratoGenerico(
                    contrato_id=r["id"],
                    user_id=r["user_id"],
                    nome=r["nome"],
                    data_vencimento=r["data_vencimento"],
                    valor=r["valor"],
                    periodicidade=r["periodicidade"],
                    tag=r["tag"],
                    usuario_compartilhado=r.get("usuario_compartilhado") or "",
                    favorito=1 if r.get("favorito") else 0,
                )
                for r in rows
            ]
        return [c for c in self.contratos if c.user_id == user_id]

    def remover_contrato(self, contrato_id: int):
        if self.dao:
            self.dao.delete_contrato(contrato_id)
            return
        self.contratos = [c for c in self.contratos if c.id != contrato_id]

    def toggle_favorito(self, contrato_id: int, user_id: int):
        if self.dao:
            self.dao.toggle_favorito(contrato_id)
            return
        for c in self.contratos:
            if c.id == contrato_id and c.user_id == user_id:
                c.favorito = 0 if c.favorito == 1 else 1
                break

    def editar_contrato(
        self,
        contrato_id: int,
        user_id: int,
        nome: str,
        data_vencimento: str,
        valor: float,
        periodicidade: str,
        tag: str,
        usuario_compartilhado: str = "",
        favorito: int = 0,
    ):
        contrato = ContratoGenerico(
            nome=nome,
            valor=valor,
            data_vencimento=data_vencimento,
            periodicidade=periodicidade,
            tag=tag,
            usuario_compartilhado=usuario_compartilhado,
            favorito=favorito,
            contrato_id=contrato_id,
            user_id=user_id,
        )
        if self.dao:
            self.dao.update_contrato(contrato)
            return True
        for i, c in enumerate(self.contratos):
            if c.id == contrato_id and c.user_id == user_id:
                self.contratos[i] = contrato
                break
        return True
