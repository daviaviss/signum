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
        self.register()

    def handle_login(self):
        self.login()

    def register(self):
        # Validate fields first
        is_valid, error_message = self.view.register_view.validate_fields()
        if not is_valid:
            self.view.show_error("Erro de Validação", error_message)
            return

        # Get validated values
        nome = self.view.register_view.get_field_value(self.view.reg_name)
        email = self.view.register_view.get_field_value(self.view.reg_email)
        senha = self.view.register_view.get_field_value(self.view.reg_password)

        if self.model.register_user(nome, email, senha):
            self.view.show_message("Sucesso", "Usuário registrado com sucesso!")
            self.view.show_login_screen()
        else:
            self.view.show_error("Erro", "Email já cadastrado.")

    def login(self):
        # Validate fields first
        is_valid, error_message = self.view.login_view.validate_fields()
        if not is_valid:
            self.view.show_error("Erro de Validação", error_message)
            return

        # Get validated values
        email = self.view.login_view.get_field_value(self.view.login_email)
        senha = self.view.login_view.get_field_value(self.view.login_password)

        if self.model.login_user(email, senha):
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
            self.view.show_error("Erro", "Email ou senha incorretos.")
