class UserLoginController:
    """
    Controller connects View and Model.
    Handles user input events and updates DB through the Model.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Bind buttons
        self.view.register_button.config(command=self.handle_register)
        self.view.login_button.config(command=self.handle_login)

    def handle_register(self):
        name = self.view.reg_name.get()
        email = self.view.reg_email.get()
        password = self.view.reg_password.get()

        if not name or not email or not password:
            self.view.show_error("Error", "All fields are required")
            return

        success = self.model.register_user(name, email, password)
        if success:
            self.view.show_message("Success", "User registered successfully!")
            self.view.show_login_screen()
        else:
            self.view.show_error("Error", "Email already exists")

    def handle_login(self):
        email = self.view.login_email.get()
        password = self.view.login_password.get()

        if not email or not password:
            self.view.show_error("Error", "All fields are required")
            return

        success = self.model.login_user(email, password)
        if success:
            # Vincula o usuário ao controller usado pela tela Metas
            uc = getattr(self.view, "usuario_controller", None)
            if uc is not None:
                usuario = uc.carregar_por_email(email)  # carrega do DAO com limites
                if usuario is None:
                    self.view.show_error("Erro", "Usuário não encontrado no banco após login.")
                    return

            # Agora o uc.usuario tem limite_assinaturas/limite_contratos carregados
            self.view.show_home_screen()
        else:
            self.view.show_error("Error", "Invalid email or password")
