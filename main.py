import os
import tkinter as tk
from mvc.models.usuario_login_model import UserLoginModel
from mvc.views.usuario_login_view import UserLoginView
from mvc.controllers.usuario_login_controller import UserLoginController

# garante que "static/arquivo.png" funcione em qualquer execução
os.chdir(os.path.dirname(__file__))

if __name__ == "__main__":
    root = tk.Tk()
    model = UserLoginModel()
    view = UserLoginView(root)
    controller = UserLoginController(model, view)
    root.mainloop()
