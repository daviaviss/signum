from dao import UserDAO
from mvc.models.usuario_model import Usuario

class UserLoginModel:
    """
    Model que manipula usuários: registro e login
    """
    def __init__(self):
        self.dao = UserDAO()

    def register_user(self, nome: str, email: str, senha: str) -> bool:
        if self.dao.get_user_by_email(email):
            return False  # usuário já existe
        user = Usuario(nome=nome, email=email, senha=senha)
        self.dao.add_user(user)
        return True

    def login_user(self, email: str, senha: str) -> bool:
        user = self.dao.get_user_by_email(email)
        if not user:
            return False
        return user.verify_password(senha)