# Documentação de Classes - Sistema Signum

## Índice
1. [Models](#models)
   - [Contrato](#contrato)
   - [Assinatura](#assinatura)
   - [PagamentoModel](#pagamentomodel)
   - [Usuario](#usuario)
   - [UserLoginModel](#userloginmodel)
2. [Controllers](#controllers)
   - [AssinaturasController](#assinaturascontroller)
   - [ContratosController](#contratoscontroller)
   - [PagamentosController](#pagamentoscontroller)
   - [UsuarioController](#usuariocontroller)
   - [UserLoginController](#userlogincontroller)
3. [Views](#views)
   - [AssinaturasView](#assinaturasview)
   - [ContratosView](#contratosview)
   - [LoginView](#loginview)
   - [RegisterView](#registerview)
   - [HomeView](#homeview)
   - [MetasView](#metasview)
   - [PerfilView](#perfilview)
   - [PagamentosView](#pagamentosview)
   - [NavbarView](#navbarview)
4. [DAOs](#daos)
   - [UserDAO](#userdao)
   - [PagamentosDAO](#pagamentosdao)
   - [AssinaturasDAO](#assinaturasdao)
   - [ContratosDAO](#contratosdao)
5. [Enums](#enums)
   - [CategoriaAssinatura](#categoriaassinatura)
   - [StatusAssinatura](#statusassinatura)
   - [CategoriaContrato](#categoriacontrato)
   - [StatusContrato](#statuscontrato)
   - [FormaPagamento](#formapagamento)
   - [Periodicidade](#periodicidade)

---

## Models

### Contrato
**Arquivo:** `mvc/models/contratos_model.py`

**Descrição:** Classe concreta para Contrato (sem pagamento/login/senha).

**Atributos:**
- `id` (int): ID do contrato
- `user_id` (int): ID do usuário proprietário
- `nome` (str): Nome do contrato
- `valor` (float): Valor do contrato
- `data_vencimento` (str): Data de vencimento
- `periodicidade` (str): Periodicidade do contrato
- `tag` (str): Categoria/tag do contrato
- `usuario_compartilhado` (str): Email do usuário compartilhado
- `favorito` (int): Flag de favorito (0 ou 1)
- `status` (StatusContrato): Status do contrato (Ativo/Encerrado)

**Propriedades:**
- `tipo` (str): Retorna "contrato"

**Métodos:**
- `__init__(nome: str, valor: float, data_vencimento: str, periodicidade: str, tag: str, usuario_compartilhado: str = "", favorito: int = 0, contrato_id: int = None, user_id: int = None, status: StatusContrato = StatusContrato.ATIVO)`: Construtor da classe
- `__repr__() -> str`: Representação em string do objeto

---

### Assinatura
**Arquivo:** `mvc/models/assinaturas_model.py`

**Herda de:** `Contrato`

**Descrição:** Model para Assinatura - herda de Contrato e adiciona login/senha e forma de pagamento.

**Atributos adicionais (além dos herdados de Contrato):**
- `forma_pagamento` (str): Nome do método de pagamento (referência a um `PagamentoModel` cadastrado)
- `login` (str): Login da assinatura
- `senha` (str): Senha da assinatura
- `created_at` (str): Data de criação (ISO format)
- `is_readonly` (bool): Flag indicando se é somente leitura

**Propriedades:**
- `tipo` (str): Retorna "assinatura" (sobrescreve Contrato)

**Métodos:**
- `__init__(nome: str, data_vencimento: str, valor: float, periodicidade: str, tag: str, forma_pagamento: str, usuario_compartilhado: str = "", login: str = "", senha: str = "", favorito: int = 0, assinatura_id: int = None, user_id: int = None, status = None, created_at: str = None)`: Construtor da classe (status padrão = ATIVO)
- `__repr__() -> str`: Representação em string do objeto

---

### PagamentoModel
**Arquivo:** `mvc/models/pagamentos_model.py`

**Descrição:** Modelo para representar informações de pagamento.

**Atributos privados:**
- `_nome` (str): Nome associado ao pagamento
- `_vencimento` (date): Data de vencimento do pagamento
- `_forma_de_pagamento` (FormaPagamento): Forma de pagamento selecionada

**Propriedades:**
- `nome` (str): Nome associado ao pagamento (getter/setter)
- `vencimento` (date): Data de vencimento do pagamento (getter/setter)
- `forma_de_pagamento` (FormaPagamento): Forma de pagamento selecionada (getter/setter)

**Métodos:**
- `__init__(nome: str, vencimento: date, forma_de_pagamento: FormaPagamento)`: Construtor da classe

**Validações:**
- Nome: deve ser string não vazia, capitaliza primeira letra
- Vencimento: deve ser objeto date ou None
- Forma de pagamento: deve ser enum FormaPagamento

---

### Usuario
**Arquivo:** `mvc/models/usuario_model.py`

**Descrição:** Model para representar um usuário do sistema.

**Atributos:**
- `id` (int): ID do usuário
- `nome` (str): Nome do usuário
- `email` (str): Email do usuário
- `senha_hash` (str): Hash da senha (salt + hash)
- `_limite_assinaturas` (float): Limite de gastos com assinaturas
- `_limite_contratos` (float): Limite de gastos com contratos

**Propriedades:**
- `limite_assinaturas` (float): Getter/setter para limite de assinaturas (valida se >= 0)
- `limite_contratos` (float): Getter/setter para limite de contratos (valida se >= 0)

**Métodos:**
- `__init__(nome: str, email: str, senha: str, user_id: int = None, limite_assinaturas: float = 0.0, limite_contratos: float = 0.0)`: Construtor
- `_hash_password(senha: str) -> str`: Cria hash seguro usando sha256 + salt
- `verify_password(senha: str) -> bool`: Verifica se senha fornecida bate com hash salvo
- `__repr__() -> str`: Representação em string do objeto

---

### UserLoginModel
**Arquivo:** `mvc/models/usuario_login_model.py`

**Descrição:** Model que manipula usuários: registro e login.

**Atributos:**
- `dao` (UserDAO): Instância do DAO de usuários

**Métodos:**
- `__init__()`: Inicializa o model com UserDAO
- `register_user(nome: str, email: str, senha: str) -> bool`: Registra novo usuário (retorna False se email já existe)
- `login_user(email: str, senha: str) -> bool`: Valida credenciais de login (retorna True se válido)

---

## Controllers

### AssinaturasController
**Arquivo:** `mvc/controllers/assinaturas_controller.py`

**Descrição:** Controller para Assinaturas.

**Atributos:**
- `view` (AssinaturasView): Referência para a view
- `user_id` (int): ID do usuário logado
- `usuario_controller` (UsuarioController): Referência para UsuarioController
- `dao` (AssinaturasDAO): Instância do DAO de assinaturas
- `pagamentos_controller` (PagamentosController): Controller de pagamentos

**Métodos públicos:**
- `__init__(view: AssinaturasView, user_id: int = None, usuario_controller: UsuarioController = None)`: Inicializa controller
- `mostrar_sucesso(titulo: str, mensagem: str) -> None` (estático): Exibe mensagem de sucesso
- `mostrar_erro(titulo: str, mensagem: str) -> None` (estático): Exibe mensagem de erro
- `mostrar_aviso(titulo: str, mensagem: str) -> None` (estático): Exibe mensagem de aviso
- `confirmar_acao(titulo: str, mensagem: str) -> bool` (estático): Exibe diálogo de confirmação
- `exibir_erro_validacao(validacao: dict) -> None`: Exibe erro baseado em código de validação
- `calcular_total_assinaturas(assinaturas: List[Assinatura] = None) -> float`: Calcula valor total de assinaturas ativas
- `calcular_diferenca_meta() -> float`: Calcula diferença entre meta e total ativo
- `obter_dados_formulario() -> dict`: Extrai dados do formulário da view
- `validar_dados_formulario(data: dict, assinatura_id: int = None) -> dict`: Validação completa do formulário
- `limpar_formulario() -> None`: Limpa campos do formulário
- `adicionar(nome: str, data_vencimento: str, valor: float, periodicidade: str, categoria: str, forma_pagamento: str, usuario_compartilhado: str = "", login: str = "", senha: str = "") -> dict`: Adiciona nova assinatura
- `remover(assinatura_id: int) -> dict`: Remove assinatura (apenas se status ENCERRADO)
- `alternar_favorito(assinatura_id: int) -> None`: Alterna status de favorito
- `renovar_vencimento_se_necessario(assinatura_id: int) -> bool`: Renova vencimento se passou
- `renovar_todas_assinaturas_ativas() -> None`: Renova todas assinaturas vencidas
- `editar(assinatura_id: int, nome: str, data_vencimento: str, valor: float, periodicidade: str, categoria: str, forma_pagamento: str, usuario_compartilhado: str = "", login: str = "", senha: str = "", favorito: int = 0, status: StatusAssinatura = None) -> dict`: Edita assinatura existente
- `obter_categorias_disponiveis() -> List[str]`: Retorna lista de categorias
- `obter_periodicidades() -> List[str]`: Retorna lista de periodicidades
- `obter_formas_pagamento() -> List[str]`: Retorna lista de formas de pagamento
- `processar_compartilhamento(assinatura_id: int, email_compartilhado: str) -> dict`: Processa compartilhamento

**Métodos privados:**
- `_exibir_erro_campos_obrigatorios(mensagem: str) -> None`: Exibe erro de campos obrigatórios
- `_exibir_erro_valor_invalido(mensagem: str) -> None`: Exibe erro de valor inválido
- `_exibir_erro_data_invalida(mensagem: str) -> None`: Exibe erro de data inválida
- `_exibir_erro_nome_duplicado(mensagem: str) -> None`: Exibe erro de nome duplicado
- `_exibir_erro_generico(mensagem: str) -> None`: Exibe erro genérico
- `_obter_mapeamento_erros_validacao() -> dict`: Retorna dict de error_code → método
- `_carregar_assinaturas() -> None`: Carrega e exibe assinaturas do usuário
- `_validar_data(date_str: str) -> dict`: Valida formato e valor da data
- `_verificar_nome_duplicado(nome: str, assinatura_id: int = None) -> dict`: Verifica duplicidade de nome
- `_validar_campos_obrigatorios(data: dict) -> dict`: Valida campos obrigatórios
- `_validar_formato_valor(data: dict) -> dict`: Valida formato do valor
- `_validar_formato_data(data: dict) -> dict`: Valida formato da data
- `_validar_data_nao_futura(date_obj: date) -> dict`: Valida se data >= hoje
- `_validar_nome_unico(data: dict, assinatura_id: int = None) -> dict`: Valida unicidade do nome
- `_criar_objeto_assinatura(nome: str, data_vencimento: str, valor: float, periodicidade: str, categoria: str, forma_pagamento: str, usuario_compartilhado: str = "", login: str = "", senha: str = "", favorito: int = 0, status: StatusAssinatura = None, assinatura_id: int = None) -> Assinatura`: Cria objeto Assinatura
- `_finalizar_operacao(assinatura_id: int, usuario_compartilhado: str, mensagem_sucesso: str) -> dict`: Finaliza operação
- `_pode_remover_assinatura(assinatura_id: int) -> dict`: Verifica se pode remover
- `_ultimo_dia_mes(ano: int, mes: int) -> int`: Retorna último dia do mês
- `_calcular_proxima_data(data_atual: date, periodicidade: str) -> date`: Calcula próxima data
- `_validar_compartilhamento(email_compartilhado: str) -> dict`: Valida dados de compartilhamento
- `_criar_compartilhamento_assinatura(assinatura_id: int, user_id_compartilhado: int, email_compartilhado: str) -> dict`: Cria compartilhamento no BD

---

### ContratosController
**Arquivo:** `mvc/controllers/contratos_controller.py`

**Descrição:** Controller para Contratos (genérico, sem pagamento/login/senha).

**Atributos:**
- `view` (ContratosView): Referência para a view
- `user_id` (int): ID do usuário logado
- `dao` (ContratosDAO): Instância do DAO de contratos

**Métodos públicos:**
- `__init__(view: ContratosView, user_id: int = None)`: Inicializa controller
- `adicionar(nome: str, data_vencimento: str, valor: float, periodicidade: str, tag: str, usuario_compartilhado: str = "") -> bool`: Adiciona novo contrato
- `remover(contrato_id: int) -> None`: Remove contrato
- `toggle_favorito(contrato_id: int) -> None`: Alterna status de favorito
- `editar(contrato_id: int, nome: str, data_vencimento: str, valor: float, periodicidade: str, tag: str, usuario_compartilhado: str = "", favorito: int = 0) -> bool`: Edita contrato existente
- `get_tags_disponiveis() -> List[str]`: Retorna lista de tags disponíveis
- `get_periodicidades() -> List[str]`: Retorna lista de periodicidades

**Métodos privados:**
- `_carregar_contratos() -> None`: Carrega e exibe contratos do usuário
---

### PagamentosController
**Arquivo:** `mvc/controllers/pagamentos_controller.py`

**Descrição:** Controlador para gerenciar operações relacionadas a pagamentos.

**Atributos:**
- `dao` (PagamentosDAO): Instância do DAO de pagamentos

**Métodos públicos:**
- `__init__()`: Inicializa controller
- `criar_pagamento(nome: str, vencimento: Optional[date], forma_pagamento: FormaPagamento) -> int`: Cria novo pagamento
- `listar_pagamentos() -> List[PagamentoModel]`: Lista todos os pagamentos cadastrados
- `atualizar_pagamento(pagamento_id: int, nome: str, vencimento: Optional[date], forma_pagamento: FormaPagamento) -> None`: Atualiza pagamento existente
- `excluir_pagamento(pagamento_id: int) -> None`: Exclui pagamento
- `obter_nomes_metodos_pagamento() -> List[str]`: Retorna lista com nomes dos métodos de pagamento

---

### UsuarioController
**Arquivo:** `mvc/controllers/usuario_controller.py`

**Descrição:** Controller para operações do usuário já autenticado (não cuida de login).

**Atributos:**
- `usuario` (Usuario): Usuário vinculado ao controller
- `dao` (UserDAO): Instância do DAO de usuários

**Métodos públicos:**
- `__init__(usuario: Optional[Usuario] = None, dao: Optional[UserDAO] = None)`: Inicializa controller
- `bind_usuario(usuario: Usuario) -> None`: Vincula usuário logado ao controller
- `logout() -> None`: Desvincula usuário (logout)
- `carregar_por_email(email: str) -> Optional[Usuario]`: Carrega usuário por email e vincula
- `get_limite_assinaturas() -> float`: Retorna limite de assinaturas
- `get_limite_contratos() -> float`: Retorna limite de contratos
- `definir_limite_assinaturas(novo_limite: float) -> float`: Define e persiste limite de assinaturas
- `definir_limite_contratos(novo_limite: float) -> float`: Define e persiste limite de contratos
- `update_profile(new_name: str, new_email: str, new_password: str = None) -> None`: Atualiza perfil do usuário

**Métodos privados:**
- `_persistir_limites() -> None`: Persiste limites no banco
- `_garante_usuario() -> None`: Valida se usuário está vinculado

---

### UserLoginController
**Arquivo:** `mvc/controllers/usuario_login_controller.py`

**Descrição:** Controller conecta View e Model para login/registro.

**Atributos:**
- `model` (UserLoginModel): Model de login
- `view` (HomeView): Referência para a view

**Métodos públicos:**
- `__init__(model: UserLoginModel, view: HomeView)`: Inicializa controller e vincula botões
- `handle_register() -> None`: Handler do botão de registro
- `handle_login() -> None`: Handler do botão de login
- `register() -> None`: Executa registro de usuário
- `login() -> None`: Executa login de usuário
- `logout() -> None`: Efetua logout

---

## Views

### AssinaturasView
**Arquivo:** `mvc/views/assinaturas_view.py`

**Descrição:** View para tela de Assinaturas.

**Atributos:**
- `parent`: tk.Widget - Widget pai do Tkinter
- `controller`: AssinaturasController - Controlador da view
- `assinaturas_data`: List[Assinatura] - Dados completos das assinaturas para ordenação
- `sort_reverse`: Dict[str, bool] - Rastreia direção de ordenação por coluna
- `entry_nome`: tk.Entry - Campo de entrada do nome
- `entry_valor`: tk.Entry - Campo de entrada do valor
- `entry_data`: tk.Entry - Campo de entrada da data
- `combo_periodicidade`: ttk.Combobox - Combobox de periodicidade
- `combo_categoria`: ttk.Combobox - Combobox de categoria
- `combo_pagamento`: ttk.Combobox - Combobox de forma de pagamento
- `entry_usuario_compartilhado`: tk.Entry - Campo de email compartilhado
- `entry_login`: tk.Entry - Campo de login
- `entry_senha`: tk.Entry - Campo de senha
- `tree`: ttk.Treeview - Tabela de assinaturas

**Métodos públicos:**
- `__init__(parent: tk.Widget, controller: AssinaturasController = None) -> None`: Inicializa a view
- `set_combo_values(periodicidades: List[str], categorias: List[str], pagamentos: List[str]) -> None`: Define valores dos comboboxes
- `atualizar_lista(assinaturas: List[Assinatura]) -> None`: Atualiza a lista de assinaturas exibida
- `limpar_campos() -> None`: Limpa todos os campos do formulário

**Métodos privados:**
- `_create_ui() -> None`: Cria a interface da tela
- `_create_form(parent: tk.Widget) -> None`: Cria o formulário de assinaturas
- `_create_treeview(parent: tk.Widget) -> None`: Cria a tabela de assinaturas
- `_ao_adicionar() -> None`: Handler do botão adicionar
- `_ordenar_coluna(col: str) -> None`: Ordena a tabela por coluna
- `_on_double_click(event: tk.Event) -> None`: Handler de duplo clique na tabela
- `_on_right_click(event: tk.Event) -> None`: Handler de clique direito na tabela

---

### ContratosView
**Arquivo:** `mvc/views/contratos_view.py`

**Herda de:** `AssinaturasView`

**Descrição:** View para tela de Contratos, espelhando AssinaturasView mas sem campos de pagamento/login/senha.

**Atributos:** (Mesmos da classe pai AssinaturasView com tipagem completa, exceto sem entry_login, entry_senha e combo_pagamento)
- `parent`: tk.Widget - Widget pai do Tkinter (herdado)
- `controller`: ContratosController - Controlador da view
- `assinaturas_data`: List[Contrato] - Dados completos dos contratos para ordenação (herdado)
- `sort_reverse`: Dict[str, bool] - Rastreia direção de ordenação por coluna (herdado)
- `entry_nome`: tk.Entry - Campo de entrada do nome (herdado)
- `entry_valor`: tk.Entry - Campo de entrada do valor (herdado)
- `entry_data`: tk.Entry - Campo de entrada da data (herdado)
- `combo_periodicidade`: ttk.Combobox - Combobox de periodicidade (herdado)
- `combo_categoria`: ttk.Combobox - Combobox de categoria (herdado)
- `tree`: ttk.Treeview - Tabela de contratos (herdado)

**Métodos públicos:**
- `__init__(parent: tk.Widget, controller: ContratosController = None) -> None`: Inicializa a view

**Métodos privados:**
- `_create_ui() -> None`: Cria a interface da tela (sobrescreve)
- `_create_form(parent: tk.Widget) -> None`: Cria o formulário de contratos sem pagamento/login/senha (sobrescreve)

---

### LoginView
**Arquivo:** `mvc/views/login_view.py`

**Descrição:** View para tela de login do usuário.

**Atributos:**
- `parent`: tk.Widget - Widget pai do Tkinter
- `switch_to_register_callback`: Callable[[], None] - Callback para trocar para tela de registro
- `frame`: tk.Frame - Frame principal da view
- `login_email`: tk.Entry - Campo de entrada do email
- `login_password`: tk.Entry - Campo de entrada da senha
- `login_button`: tk.Button - Botão de login
- `switch_to_register_button`: tk.Button - Botão para ir ao registro
- `_placeholders`: Dict[tk.Entry, str] - Dicionário de placeholders dos campos

**Métodos públicos:**
- `__init__(parent: tk.Widget, switch_to_register_callback: Callable[[], None]) -> None`: Inicializa a view
- `get_field_value(entry: tk.Entry) -> str`: Retorna valor do campo (vazio se for placeholder)
- `validate_fields() -> Tuple[bool, str]`: Valida se campos estão preenchidos corretamente
- `show() -> None`: Exibe a view

**Métodos privados:**
- `_add_placeholder(entry: tk.Entry, text: str) -> None`: Adiciona placeholder ao campo
- `_create_ui() -> None`: Cria a interface da tela

---

### RegisterView
**Arquivo:** `mvc/views/register_view.py`

**Descrição:** View para tela de registro de novo usuário.

**Atributos:**
- `parent`: tk.Widget - Widget pai do Tkinter
- `switch_to_login_callback`: Callable[[], None] - Callback para trocar para tela de login
- `frame`: tk.Frame - Frame principal da view
- `reg_name`: tk.Entry - Campo de entrada do nome
- `reg_email`: tk.Entry - Campo de entrada do email
- `reg_password`: tk.Entry - Campo de entrada da senha
- `register_button`: tk.Button - Botão de registro
- `switch_to_login_button`: tk.Button - Botão para ir ao login
- `_placeholders`: Dict[tk.Entry, str] - Dicionário de placeholders dos campos

**Métodos públicos:**
- `__init__(parent: tk.Widget, switch_to_login_callback: Callable[[], None]) -> None`: Inicializa a view
- `get_field_value(entry: tk.Entry) -> str`: Retorna valor do campo (vazio se for placeholder)
- `validate_fields() -> Tuple[bool, str]`: Valida se campos estão preenchidos corretamente
- `show() -> None`: Exibe a view

**Métodos privados:**
- `_add_placeholder(entry: tk.Entry, text: str) -> None`: Adiciona placeholder ao campo
- `_create_ui() -> None`: Cria a interface da tela

---

### HomeView
**Arquivo:** `mvc/views/home_view.py`

**Descrição:** View para tela principal com navegação.

**Atributos:**
- `parent`: tk.Widget - Widget pai do Tkinter
- `usuario_controller`: UsuarioController - Controlador do usuário
- `frame`: tk.Frame - Frame principal da view
- `navbar`: NavbarView - View da barra de navegação
- `metas_view`: MetasView - View de metas
- `perfil_view`: PerfilView - View de perfil
- `assinaturas_controller`: AssinaturasController - Controller de assinaturas
- `contratos_controller`: ContratosController - Controller de contratos
- `on_logout`: Callable[[], None] - Callback de logout
- `_home_imgs`: List[tk.PhotoImage] - Lista de imagens para manter referências

**Métodos públicos:**
- `__init__(parent: tk.Widget, usuario_controller: UsuarioController = None) -> None`: Inicializa a view
- `show() -> None`: Exibe a tela principal
- `show_home_screen() -> None`: Exibe tela inicial/dashboard
- `show_assinaturas_screen() -> None`: Exibe tela de assinaturas
- `show_contratos_screen() -> None`: Exibe tela de contratos
- `show_metas_screen() -> None`: Exibe tela de metas
- `show_profile_screen() -> None`: Exibe tela de edição de perfil
- `aside_perfil() -> None`: Cria aside lateral com informações do perfil

**Métodos privados:**
- `_render_navbar(parent: tk.Frame, active: str) -> None`: Renderiza barra de navegação
- `_on_logout() -> None`: Executa callback de logout

---

### MetasView
**Arquivo:** `mvc/views/metas_view.py`

**Descrição:** View para tela de metas/limites.

**Atributos:**
- `parent`: tk.Widget - Widget pai do Tkinter
- `usuario_controller`: UsuarioController - Controlador do usuário
- `assinaturas_controller`: AssinaturasController - Controlador de assinaturas
- `frame`: tk.Frame - Frame principal da view
- `label_meta_anual`: tk.Label - Label da meta anual
- `label_meta_mensal`: tk.Label - Label da meta mensal
- `label_gasto_anual`: tk.Label - Label do gasto anual
- `label_gasto_mensal`: tk.Label - Label do gasto mensal

**Métodos públicos:**
- `__init__(parent: tk.Widget, usuario_controller: UsuarioController, assinaturas_controller: AssinaturasController) -> None`: Inicializa a view

**Métodos privados:**
- `_create_ui() -> None`: Cria a interface da tela
- `_format_brl(valor: float) -> str`: Formata valor em BRL (R$9.999,99)
- `_format_display(valor: float) -> str`: Formata valor abreviado (R$10mil, R$1,2M)
- `_build_cards() -> None`: Monta interface dos cards de metas

---

### PerfilView
**Arquivo:** `mvc/views/perfil_view.py`

**Descrição:** View para tela de edição de perfil do usuário.

**Atributos:**
- `parent`: tk.Widget - Widget pai do Tkinter
- `usuario_controller`: UsuarioController - Controlador do usuário
- `on_back`: Callable[[], None] - Callback para voltar à tela anterior
- `frame`: tk.Frame - Frame principal da view
- `entry_nome`: tk.Entry - Campo de entrada do nome
- `entry_email`: tk.Entry - Campo de entrada do email
- `entry_meta_mensal`: tk.Entry - Campo de entrada da meta mensal
- `entry_meta_anual`: tk.Entry - Campo de entrada da meta anual
- `_placeholders`: Dict[tk.Entry, str] - Dicionário de placeholders dos campos

**Métodos públicos:**
- `__init__(parent: tk.Widget, usuario_controller: UsuarioController, on_back: Callable[[], None]) -> None`: Inicializa a view
- `get_field_value(entry: tk.Entry) -> str`: Retorna valor do campo (vazio se for placeholder)
- `save_profile() -> None`: Salva as alterações do perfil

**Métodos privados:**
- `_create_ui() -> None`: Cria a interface da tela
- `_add_placeholder(entry: tk.Entry, text: str, is_password: bool = False) -> None`: Adiciona placeholder ao campo
- `_create_profile_screen() -> None`: Cria a tela de edição de perfil

---

### PagamentosView
**Arquivo:** `mvc/views/pagamentos_view.py`

**Descrição:** View para tela de gerenciamento de métodos de pagamento.

**Atributos:**
- `parent`: tk.Widget - Widget pai do Tkinter
- `controller`: PagamentosController - Controlador de pagamentos
- `frame`: tk.Frame - Frame principal da view
- `entry_nome`: tk.Entry - Campo de entrada do nome do método de pagamento
- `tree`: ttk.Treeview - Treeview para lista de métodos de pagamento
- `btn_adicionar`: tk.Button - Botão adicionar
- `btn_editar`: tk.Button - Botão editar
- `btn_excluir`: tk.Button - Botão excluir

**Métodos públicos:**
- `__init__(parent: tk.Widget) -> None`: Inicializa a view

**Métodos privados:**
- `_create_ui() -> None`: Cria a interface da tela
- `_setup_ui() -> None`: Configura a interface do usuário
- `_load_data() -> None`: Carrega dados de pagamentos
- `_add_payment() -> None`: Adiciona novo método de pagamento
- `_edit_payment() -> None`: Edita método de pagamento selecionado
- `_delete_payment() -> None`: Remove método de pagamento

---

### NavbarView
**Arquivo:** `mvc/views/navbar_view.py`

**Descrição:** View para barra de navegação.

**Atributos:**
- `parent`: tk.Widget - Widget pai do Tkinter
- `callbacks`: Dict[str, Callable[[], None]] - Dicionário de callbacks de navegação
- `active`: str - Item ativo da navegação
- `navbar_frame`: tk.Frame - Frame da barra de navegação
- `links`: Dict[str, tk.Label] - Dicionário de labels dos links de navegação

**Métodos públicos:**
- `__init__(parent: tk.Widget, callbacks: Dict[str, Callable], active: str = "home") -> None`: Inicializa a view

**Métodos privados:**
- `_create_navbar() -> None`: Cria a barra de navegação
- `_render_navbar() -> None`: Desenha o navbar no frame pai
- `_create_link(parent: tk.Widget, text: str, callback_key: str) -> tk.Label`: Cria link de navegação
- `_call_callback(key: str) -> None`: Chama callback associado à chave
- `_show_notification_message() -> None`: Exibe mensagem de notificações

---

## DAOs

### UserDAO
**Arquivo:** `dao.py`

**Descrição:** DAO para gerenciar usuários no banco de dados.

**Atributos:**
- `conn` (sqlite3.Connection): Conexão com banco SQLite

**Métodos públicos:**
- `__init__(db_file: str = "database.sqlite")`: Inicializa DAO e cria tabela
- `add_user(user: Usuario) -> None`: Adiciona novo usuário
- `get_user_by_email(email: str) -> Optional[Usuario]`: Busca usuário por email
- `update_user_limits(user_id: int, limite_assinaturas: float, limite_contratos: float) -> None`: Atualiza limites
- `update_user_profile(user_id: int, nome: str, email: str, senha_hash: str) -> None`: Atualiza perfil
- `get_user_id_by_email(email: str) -> Optional[int]`: Retorna ID do usuário por email

**Métodos privados:**
- `_create_table() -> None`: Cria tabela users
- `_ensure_limit_columns() -> None`: Garante existência das colunas de limite

---

### PagamentosDAO
**Arquivo:** `dao.py`

**Descrição:** DAO para gerenciar pagamentos no banco de dados.

**Atributos:**
- `conn` (sqlite3.Connection): Conexão com banco SQLite

**Métodos públicos:**
- `__init__(db_file: str = "database.sqlite")`: Inicializa DAO
- `add_pagamento(pagamento: PagamentoModel) -> int`: Adiciona novo pagamento
- `get_all_pagamentos() -> List[PagamentoModel]`: Retorna todos os pagamentos ordenados por vencimento
- `update_pagamento(pagamento_id: int, pagamento: PagamentoModel) -> None`: Atualiza pagamento existente
- `delete_pagamento(pagamento_id: int) -> None`: Remove pagamento

**Métodos privados:**
- `_drop_and_create_table() -> None`: Recria tabela com schema atualizado

---

### AssinaturasDAO
**Arquivo:** `dao.py`

**Descrição:** DAO para gerenciar assinaturas no banco de dados.

**Atributos:**
- `db_file` (str): Caminho do arquivo do banco

**Métodos públicos:**
- `__init__(db_file: str = "database.sqlite")`: Inicializa DAO
- `adicionar_assinatura(assinatura: Assinatura) -> int`: Adiciona nova assinatura
- `obter_assinaturas_por_usuario(user_id: int) -> List[Assinatura]`: Retorna assinaturas do usuário
- `alternar_favorito(assinatura_id: int) -> None`: Alterna status de favorito
- `deletar_assinatura(assinatura_id: int) -> None`: Remove assinatura
- `atualizar_assinatura(assinatura: Assinatura) -> None`: Atualiza assinatura existente
- `compartilhar_assinatura(assinatura_id: int, user_id_proprietario: int, user_id_compartilhado: int) -> bool`: Compartilha assinatura
- `remover_compartilhamento(assinatura_id: int, user_id_compartilhado: int) -> None`: Remove compartilhamento
- `obter_assinaturas_compartilhadas_comigo(user_id: int) -> List[Assinatura]`: Retorna assinaturas compartilhadas comigo (readonly)

**Métodos privados:**
- `_create_table(conn: sqlite3.Connection) -> None`: Cria tabela assinaturas
- `_ensure_favorito_column(conn: sqlite3.Connection) -> None`: Garante coluna favorito
- `_ensure_status_column(conn: sqlite3.Connection) -> None`: Garante coluna status
- `_ensure_created_at_column(conn: sqlite3.Connection) -> None`: Garante coluna created_at
- `_create_compartilhamentos_table(conn: sqlite3.Connection) -> None`: Cria tabela de compartilhamentos

---

### ContratosDAO
**Arquivo:** `dao.py`

**Descrição:** DAO para gerenciar contratos no banco de dados.

**Atributos:**
- `conn` (sqlite3.Connection): Conexão com banco SQLite

**Métodos públicos:**
- `__init__(db_file: str = "database.sqlite")`: Inicializa DAO
- `add_contrato(contrato: Contrato) -> int`: Adiciona novo contrato
- `get_contratos_by_user(user_id: int) -> List[dict]`: Retorna contratos do usuário
- `toggle_favorito(contrato_id: int) -> None`: Alterna status de favorito
- `delete_contrato(contrato_id: int) -> None`: Remove contrato
- `update_contrato(contrato: Contrato) -> None`: Atualiza contrato existente

**Métodos privados:**
- `_create_table() -> None`: Cria tabela contratos
- `_ensure_favorito_column() -> None`: Garante coluna favorito
- `_ensure_status_column() -> None`: Garante coluna status
- `_migrate_schema() -> None`: Migra schema antigo

---

## Enums

### CategoriaAssinatura
**Arquivo:** `mvc/models/assinatura_categoria_enum.py`

**Descrição:** Enum que define categorias de assinatura.

**Valores:**
- `STREAMING = "Streaming"`
- `CLUBES = "Clubes"`
- `ALIMENTACAO = "Alimentação"`
- `SAAS = "SaaS"`
- `PETS = "Pets"`
- `OUTROS = "Outros"`

---

### StatusAssinatura
**Arquivo:** `mvc/models/assinatura_status_enum.py`

**Descrição:** Enum que define os status possíveis de uma assinatura.

**Valores:**
- `ATIVO = "Ativo"`
- `ENCERRADO = "Encerrado"`

---

### CategoriaContrato
**Arquivo:** `mvc/models/contrato_categoria_enum.py`

**Descrição:** Enum para categorias de contratos.

**Valores:**
- `SERVICOS_PROFISSIONAIS = "Serviços profissionais"`
- `EDUCACAO = "Educação"`
- `FINANCIAMENTO = "Financiamento"`
- `SAUDE = "Saude"`
- `ALUGUEL = "Aluguel"`
- `OUTROS = "Outros"`

---

### StatusContrato
**Arquivo:** `mvc/models/contrato_status_enum.py`

**Descrição:** Enum que define os status possíveis de um contrato.

**Valores:**
- `ATIVO = "Ativo"`
- `ENCERRADO = "Encerrado"`

---

### FormaPagamento
**Arquivo:** `mvc/models/forma_pagamento_enum.py`

**Descrição:** Enum que define as formas de pagamento disponíveis.

**Valores:**
- `DINHEIRO = "Dinheiro"`
- `CARTAO_CREDITO = "Cartão de crédito"`
- `CARTAO_DEBITO = "Cartão de débito"`
- `PIX = "PIX"`
- `GIFT_CARD = "Gift card"`
- `OUTROS = "Outros"`

---

### Periodicidade
**Arquivo:** `mvc/models/periodicidade_enum.py`

**Descrição:** Enum para periodicidades de contratos e assinaturas.

**Valores:**
- `MENSAL = "Mensal"`
- `TRIMESTRAL = "Trimestral"`
- `SEMESTRAL = "Semestral"`
- `ANUAL = "Anual"`

---

## Resumo Estatístico

**Total de Classes:** 15
- Models: 5
- Controllers: 5
- DAOs: 4
- Enums: 6 (não contabilizados como classes tradicionais)

**Total de Métodos:** 135+
- AssinaturasController: 46 métodos
- ContratosController: 7 métodos
- PagamentosController: 5 métodos
- UsuarioController: 11 métodos
- UserLoginController: 4 métodos
- UserDAO: 6 métodos
- PagamentosDAO: 4 métodos
- AssinaturasDAO: 10 métodos
- ContratosDAO: 8 métodos
