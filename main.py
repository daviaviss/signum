import os
import tkinter as tk
from mvc.models.usuario_login_model import UserLoginModel
from mvc.controllers.navegacao_controller import NavegacaoController
from mvc.controllers.usuario_login_controller import UserLoginController
from mvc.controllers.usuario_controller import UsuarioController 

# garante que "static/arquivo.png" funcione em qualquer execução
os.chdir(os.path.dirname(__file__))

if __name__ == "__main__":
    root = tk.Tk()
    model = UserLoginModel()
    navegacao = NavegacaoController(root)
    controller = UserLoginController(model, navegacao)
    
    # passa o model para o controller de usuário para que ele saiba quem está logado
    usuario_controller = UsuarioController(model)
    navegacao.usuario_controller = usuario_controller  # passa o controller para a navegação
    navegacao.home_view.on_logout = controller.logout
    root.mainloop()
