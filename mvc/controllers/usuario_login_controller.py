class UserLoginController:
    """
    Controller para funcionalidade de login e registro.
    Gerencia eventos de entrada do usuário e atualiza o BD através do Model.
    Trabalha com NavegacaoController para gerenciar transições de tela.
    """
    def __init__(self, model, navegacao):
        self.model = model
        self.navegacao = navegacao

        # Bind buttons
        self.navegacao.register_button.config(command=self.handle_register)
        self.navegacao.login_button.config(command=self.handle_login)

    def handle_register(self):
        self.register()

    def handle_login(self):
        self.login()

    def register(self):
        # Validate fields first
        is_valid, error_message = self.navegacao.register_view.validate_fields()
        if not is_valid:
            self.navegacao.mostrar_erro("Erro de Validação", error_message)
            return

        # Get validated values
        nome = self.navegacao.register_view.get_field_value(self.navegacao.reg_name)
        email = self.navegacao.register_view.get_field_value(self.navegacao.reg_email)
        senha = self.navegacao.register_view.get_field_value(self.navegacao.reg_password)

        if self.model.register_user(nome, email, senha):
            self.navegacao.mostrar_mensagem("Sucesso", "Usuário registrado com sucesso!")
            self.navegacao.mostrar_tela_login()
        else:
            self.navegacao.mostrar_erro("Erro", "Email já cadastrado.")

    def login(self):
        # Validate fields first
        is_valid, error_message = self.navegacao.login_view.validate_fields()
        if not is_valid:
            self.navegacao.mostrar_erro("Erro de Validação", error_message)
            return

        # Get validated values
        email = self.navegacao.login_view.get_field_value(self.navegacao.login_email)
        senha = self.navegacao.login_view.get_field_value(self.navegacao.login_password)

        if self.model.login_user(email, senha):
            # Vincula o usuário ao controller usado pela tela Metas
            uc = getattr(self.navegacao, "usuario_controller", None)
            if uc is not None:
                usuario = uc.carregar_por_email(email)  # carrega do DAO com limites
                if usuario is None:
                    self.navegacao.mostrar_erro("Erro", "Usuário não encontrado no banco após login.")
                    return

            # Agora o uc.usuario tem limite_assinaturas/limite_contratos carregados
            self.navegacao.mostrar_tela_home()
        else:
            self.navegacao.mostrar_erro("Erro", "Email ou senha incorretos.")

    def logout(self):
        """Efetua logout e retorna à tela de login."""
        uc = getattr(self.navegacao, "usuario_controller", None)
        if uc is not None:
            uc.logout()
        self.navegacao.mostrar_tela_login()
