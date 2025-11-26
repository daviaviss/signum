from tkinter import messagebox
from mvc import ui_constants as UI
from mvc.views.register_view import RegisterView
from mvc.views.login_view import LoginView
from mvc.views.home_view import HomeView


class NavegacaoController:
    """
    Controller responsável por gerenciar a navegação entre as telas de login, registro e home.
    Coordena o fluxo principal da aplicação e transições entre telas.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Signum")
        self.root.geometry(f"{UI.WIDTH}x{UI.HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=UI.BG_COLOR)

        # Cria as três views
        self.register_view = RegisterView(root, self.mostrar_tela_login)
        self.login_view = LoginView(root, self.mostrar_tela_registro)
        self.home_view = HomeView(root)

        # Inicia com a tela de login
        self.mostrar_tela_login()

    def mostrar_tela_registro(self):
        self.login_view.hide()
        self.home_view.hide()
        self.register_view.show()

    def mostrar_tela_login(self):
        self.register_view.hide()
        self.home_view.hide()
        self.login_view.show()

    def mostrar_tela_home(self):
        self.register_view.hide()
        self.login_view.hide()
        # Passa usuario_controller para home_view se existir
        if hasattr(self, 'usuario_controller'):
            self.home_view.usuario_controller = self.usuario_controller
        self.home_view.show()
        self.home_view.show_home_screen()

    def mostrar_mensagem(self, title, message):
        messagebox.showinfo(title, message)

    def mostrar_erro(self, title, message):
        messagebox.showerror(title, message)

    # Expõe campos de entrada para vinculação com controller
    @property
    def reg_name(self):
        return self.register_view.reg_name

    @property
    def reg_email(self):
        return self.register_view.reg_email

    @property
    def reg_password(self):
        return self.register_view.reg_password

    @property
    def register_button(self):
        return self.register_view.register_button

    @property
    def login_email(self):
        return self.login_view.login_email

    @property
    def login_password(self):
        return self.login_view.login_password

    @property
    def login_button(self):
        return self.login_view.login_button
