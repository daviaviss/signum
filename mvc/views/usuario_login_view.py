import tkinter as tk
from tkinter import messagebox
from mvc import ui_constants as UI
from mvc.views.register_view import RegisterView
from mvc.views.login_view import LoginView
from mvc.views.home_view import HomeView



class UserLoginView:
    """
    Main coordinator for login/register/home screens.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Signum")
        self.root.geometry(f"{UI.WIDTH}x{UI.HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=UI.BG_COLOR)

        # Create the three views
        self.register_view = RegisterView(root, self.show_login_screen)
        self.login_view = LoginView(root, self.show_register_screen)
        self.home_view = HomeView(root)

        # Start with login screen
        self.show_login_screen()

    def show_register_screen(self):
        self.login_view.hide()
        self.home_view.hide()
        self.register_view.show()

    def show_login_screen(self):
        self.register_view.hide()
        self.home_view.hide()
        self.login_view.show()

    def show_home_screen(self):
        self.register_view.hide()
        self.login_view.hide()
        # Pass usuario_controller to home_view if it exists
        if hasattr(self, 'usuario_controller'):
            self.home_view.usuario_controller = self.usuario_controller
        self.home_view.show()
        self.home_view.show_home_screen()

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    # Expose entry fields for controller binding
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