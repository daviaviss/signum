import os
import tkinter as tk
from mvc.models.usuario_login_model import UserLoginModel
from mvc.views.usuario_login_view import UserLoginView
from mvc.controllers.usuario_login_controller import UserLoginController
from mvc.controllers.usuario_controller import UsuarioController 

# garante que "static/arquivo.png" funcione em qualquer execução
os.chdir(os.path.dirname(__file__))

if __name__ == "__main__":
    root = tk.Tk()
    model = UserLoginModel()
    view = UserLoginView(root)
    controller = UserLoginController(model, view)
    
    usuario_controller = UsuarioController()
    view.usuario_controller = usuario_controller  # passa o controller para a view
    root.mainloop()
