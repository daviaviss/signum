# mvc/controllers/usuario_controller.py
from typing import Optional
from dao import UserDAO
from mvc.models.usuario_model import Usuario


class UsuarioController:
    """
    Controller para operações do usuário já autenticado (não cuida de login).
    - Leitura/atualização de limites (assinaturas/contratos).
    - Persiste mudanças via DAO quando possível.
    """

    def __init__(self, usuario: Optional[Usuario] = None, dao: Optional[UserDAO] = None):
        self.usuario: Optional[Usuario] = usuario
        self.dao: UserDAO = dao or UserDAO()

    # ---------------- VÍNCULO DO USUÁRIO ----------------
    def bind_usuario(self, usuario: Usuario) -> None:
        """Vincula o usuário logado a este controller."""
        self.usuario = usuario

    def carregar_por_email(self, email: str) -> Optional[Usuario]:
        """
        Carrega o usuário pelo e-mail a partir do DAO e o vincula.
        Retorna o usuário carregado (ou None).
        """
        user = self.dao.get_user_by_email(email)
        self.usuario = user
        return user

    # ---------------- GETTERS DE LIMITES ----------------
    def get_limite_assinaturas(self) -> float:
        return float(self.usuario.limite_assinaturas) if self.usuario else 0.0

    def get_limite_contratos(self) -> float:
        return float(self.usuario.limite_contratos) if self.usuario else 0.0

    # ---------------- SETTERS DE LIMITES ----------------
    def definir_limite_assinaturas(self, novo_limite: float) -> float:
        """
        Define o limite de assinaturas do usuário atual e persiste.
        """
        self._garante_usuario()
        self.usuario.limite_assinaturas = float(novo_limite)  # valida via property do model
        self._persistir_limites()
        return self.usuario.limite_assinaturas

    def definir_limite_contratos(self, novo_limite: float) -> float:
        """
        Define o limite de contratos do usuário atual e persiste.
        """
        self._garante_usuario()
        self.usuario.limite_contratos = float(novo_limite)
        self._persistir_limites()
        return self.usuario.limite_contratos

    # ---------------- PERSISTÊNCIA ----------------
    def _persistir_limites(self) -> None:
        """
        Persiste os limites no banco, se o DAO tiver método adequado.
        """
        if not self.usuario or self.usuario.id is None:
            return

        # Método específico para limites
        if hasattr(self.dao, "update_user_limits"):
            self.dao.update_user_limits(
                user_id=self.usuario.id,
                limite_assinaturas=self.usuario.limite_assinaturas,
                limite_contratos=self.usuario.limite_contratos,
            )
        # Fallback: método genérico (se existir)
        elif hasattr(self.dao, "update_user"):
            self.dao.update_user(self.usuario)

    # ---------------- UTILITÁRIO INTERNO ----------------
    def _garante_usuario(self) -> None:
        if not self.usuario:
            raise RuntimeError("Nenhum usuário vinculado ao UsuarioController.")
