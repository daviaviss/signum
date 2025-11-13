import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from typing import Tuple, Optional
from tkcalendar import DateEntry
from mvc import ui_constants as UI
from mvc.models.forma_pagamento_enum import FormaPagamento
from mvc.controllers.pagamentos_controller import PagamentosController

class PagamentosView:
    """View para gerenciamento de métodos de pagamento."""

    def __init__(self, parent):
        self.parent = parent
        self.controller = PagamentosController()
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        """Configura a interface do usuário."""
        # Título
        titulo = tk.Label(
            self.parent,
            text="Métodos de Pagamento",
            font=UI.FONT_TITLE,
            bg=UI.BG_COLOR,
            fg="#2e3047"
        )
        titulo.pack(pady=20)
        
        # Container principal com duas colunas
        main_container = tk.Frame(self.parent, bg=UI.BG_COLOR)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Coluna esquerda - Formulário
        left_frame = tk.Frame(main_container, bg=UI.BOX_BG, width=380)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)
        
        form_title = tk.Label(
            left_frame,
            text="Novo Método de Pagamento",
            font=("Inter", 16, "bold"),
            bg=UI.BOX_BG,
            fg="#2e3047"
        )
        form_title.pack(pady=15, padx=10)

        # Frame do formulário
        form_frame = tk.Frame(left_frame, bg=UI.BOX_BG)
        form_frame.pack(fill="x", padx=20)

        # Nome
        nome_frame = tk.Frame(form_frame, bg=UI.BOX_BG)
        nome_frame.pack(fill="x", pady=5)
        
        tk.Label(
            nome_frame, 
            text="Nome", 
            bg=UI.BOX_BG, 
            font=UI.FONT_LABEL
        ).pack(side="left")
        
        tk.Label(
            nome_frame,
            text="*",
            fg="#d32f2f",
            bg=UI.BOX_BG,
            font=UI.FONT_LABEL
        ).pack(side="left")

        self.nome_entry = tk.Entry(
            form_frame,
            font=UI.FONT_ENTRY,
            bg=UI.ENTRY_BG,
            fg=UI.ENTRY_FG
        )
        self.nome_entry.pack(fill="x", pady=(0, 10))

        # Forma de Pagamento
        forma_frame = tk.Frame(form_frame, bg=UI.BOX_BG)
        forma_frame.pack(fill="x", pady=5)
        
        tk.Label(
            forma_frame,
            text="Forma de Pagamento",
            bg=UI.BOX_BG,
            font=UI.FONT_LABEL
        ).pack(side="left")
        
        tk.Label(
            forma_frame,
            text="*",
            fg="#d32f2f",
            bg=UI.BOX_BG,
            font=UI.FONT_LABEL
        ).pack(side="left")

        self.forma_combo = ttk.Combobox(
            form_frame,
            values=[forma.value for forma in FormaPagamento],
            font=UI.FONT_ENTRY,
            state="readonly"
        )
        self.forma_combo.pack(fill="x", pady=(0, 10))

        # Data de Vencimento
        data_frame = tk.Frame(form_frame, bg=UI.BOX_BG)
        data_frame.pack(fill="x", pady=5)
        
        tk.Label(
            data_frame,
            text="Data de Vencimento",
            bg=UI.BOX_BG,
            font=UI.FONT_LABEL
        ).pack(side="left")

        # Checkbox para habilitar/desabilitar data
        self.tem_vencimento = tk.BooleanVar()
        self.tem_vencimento.set(False)
        
        tk.Checkbutton(
            data_frame,
            text="Definir data",
            variable=self.tem_vencimento,
            bg=UI.BOX_BG,
            command=self._toggle_data_entry
        ).pack(side="left", padx=(10, 0))

        self.data_entry = DateEntry(
            form_frame,
            font=UI.FONT_ENTRY,
            background=UI.BTN_BG,
            foreground=UI.BTN_FG,
            date_pattern='dd/mm/yyyy',
            state="disabled"
        )
        self.data_entry.pack(fill="x", pady=(0, 10))

        # Botão Adicionar
        btn_frame = tk.Frame(form_frame, bg=UI.BOX_BG)
        btn_frame.pack(fill="x", pady=20)

        add_btn = tk.Button(
            btn_frame,
            text="Adicionar",
            font=UI.FONT_BUTTON,
            bg=UI.BTN_BG,
            fg=UI.BTN_FG,
            activebackground=UI.BTN_ACTIVE_BG,
            activeforeground=UI.BTN_ACTIVE_FG,
            relief="flat",
            command=self._adicionar_pagamento
        )
        add_btn.pack(side="right")

        # Coluna direita - TreeView
        right_frame = tk.Frame(main_container, bg=UI.BG_COLOR)
        right_frame.pack(side="left", fill="both", expand=True, pady=0)

        # Frame para o treeview e scrollbars
        tree_container = tk.Frame(right_frame, bg=UI.BG_COLOR)
        tree_container.pack(fill="both", expand=True)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_container, orient="vertical")
        scrollbar_x = ttk.Scrollbar(tree_container, orient="horizontal")
        
        self.tree = ttk.Treeview(
            tree_container,
            columns=("id", "nome", "forma", "vencimento"),
            show="headings",
            height=15,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            displaycolumns=("nome", "forma", "vencimento")  # Apenas estas colunas serão exibidas
        )
        
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Posicionar scrollbars e treeview
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Configurar colunas
        self.tree.heading("nome", text="Nome")
        self.tree.heading("forma", text="Forma de Pagamento")
        self.tree.heading("vencimento", text="Vencimento")

        self.tree.column("id", width=0, stretch=False)  # Coluna oculta para o ID
        self.tree.column("nome", width=200, minwidth=150)
        self.tree.column("forma", width=200, minwidth=150)
        self.tree.column("vencimento", width=150, minwidth=100)

        # Bind duplo clique
        self.tree.bind("<Double-1>", self._on_item_double_click)

    def _on_item_double_click(self, event):
        """Trata o evento de duplo clique em um item da lista."""
        item = self.tree.selection()
        if not item:
            return
        
        try:
            values = self.tree.item(item[0]).get('values', [])
            if not values or len(values) < 1:
                self._mostrar_erro("Item inválido selecionado")
                return
                
            pagamento_id = values[0]
            if not pagamento_id:
                self._mostrar_erro("ID do pagamento não encontrado")
                return
                
            self._abrir_janela_edicao(pagamento_id)
        except (IndexError, TypeError) as e:
            self._mostrar_erro(f"Erro ao obter dados do item: {str(e)}")

    def _abrir_janela_edicao(self, pagamento_id):
        """Abre janela para editar ou excluir um pagamento."""
        pagamentos = self.controller.listar_pagamentos()
        pagamento = next((p for p in pagamentos if getattr(p, 'id', None) == pagamento_id), None)
        
        if not pagamento:
            self._mostrar_erro("Pagamento não encontrado!")
            return

        edit_window = tk.Toplevel(self.parent)
        edit_window.title("Editar Método de Pagamento")
        edit_window.configure(bg=UI.BOX_BG)
        
        # Frame principal
        main_frame = tk.Frame(edit_window, bg=UI.BOX_BG)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Nome
        nome_frame = tk.Frame(main_frame, bg=UI.BOX_BG)
        nome_frame.pack(fill="x", pady=5)
        
        tk.Label(
            nome_frame,
            text="Nome",
            bg=UI.BOX_BG,
            font=UI.FONT_LABEL
        ).pack(side="left")
        
        tk.Label(
            nome_frame,
            text="*",
            fg="#d32f2f",
            bg=UI.BOX_BG,
            font=UI.FONT_LABEL
        ).pack(side="left")

        nome_entry = tk.Entry(
            main_frame,
            font=UI.FONT_ENTRY,
            bg=UI.ENTRY_BG,
            fg=UI.ENTRY_FG
        )
        nome_entry.insert(0, pagamento.nome)
        nome_entry.pack(fill="x", pady=(0, 10))

        # Forma de Pagamento
        forma_frame = tk.Frame(main_frame, bg=UI.BOX_BG)
        forma_frame.pack(fill="x", pady=5)
        
        tk.Label(
            forma_frame,
            text="Forma de Pagamento",
            bg=UI.BOX_BG,
            font=UI.FONT_LABEL
        ).pack(side="left")
        
        tk.Label(
            forma_frame,
            text="*",
            fg="#d32f2f",
            bg=UI.BOX_BG,
            font=UI.FONT_LABEL
        ).pack(side="left")

        forma_combo = ttk.Combobox(
            main_frame,
            values=[forma.value for forma in FormaPagamento],
            font=UI.FONT_ENTRY,
            state="readonly"
        )
        forma_combo.set(pagamento.forma_de_pagamento.value)
        forma_combo.pack(fill="x", pady=(0, 10))

        # Data de Vencimento
        data_frame = tk.Frame(main_frame, bg=UI.BOX_BG)
        data_frame.pack(fill="x", pady=5)
        
        tk.Label(
            data_frame,
            text="Data de Vencimento",
            bg=UI.BOX_BG,
            font=UI.FONT_LABEL
        ).pack(side="left")

        # Checkbox para habilitar/desabilitar data
        tem_vencimento = tk.BooleanVar()
        tem_vencimento.set(pagamento.vencimento is not None)
        
        def toggle_data_entry():
            if tem_vencimento.get():
                data_entry.configure(state="normal")
            else:
                data_entry.configure(state="disabled")

        tk.Checkbutton(
            data_frame,
            text="Definir data",
            variable=tem_vencimento,
            bg=UI.BOX_BG,
            command=toggle_data_entry
        ).pack(side="left", padx=(10, 0))

        data_entry = DateEntry(
            main_frame,
            font=UI.FONT_ENTRY,
            background=UI.BTN_BG,
            foreground=UI.BTN_FG,
            date_pattern='dd/mm/yyyy',
            state="disabled" if pagamento.vencimento is None else "normal"
        )
        if pagamento.vencimento:
            data_entry.set_date(pagamento.vencimento)
        data_entry.pack(fill="x", pady=(0, 10))

        # Frame dos botões
        btn_frame = tk.Frame(main_frame, bg=UI.BOX_BG)
        btn_frame.pack(fill="x", pady=(20, 0))

        def salvar_edicao():
            nome = nome_entry.get().strip()
            forma = forma_combo.get()

            valido, data = self._validar_formulario(nome, forma, data_entry, tem_vencimento, pagamento_id)
            if not valido:
                return
            
            try:
                self.controller.atualizar_pagamento(
                    pagamento_id=pagamento_id,
                    nome=nome,
                    vencimento=data,
                    forma_pagamento=FormaPagamento(forma)
                )
                self._load_data()
                edit_window.destroy()
            except Exception as e:
                self._mostrar_erro(str(e))

        def excluir():
            if messagebox.askyesno("Confirmar", "Deseja realmente excluir este método de pagamento?"):
                try:
                    self.controller.excluir_pagamento(pagamento_id)
                    self._load_data()
                    edit_window.destroy()
                except Exception as e:
                    self._mostrar_erro(str(e))

        tk.Button(
            btn_frame,
            text="Excluir",
            font=UI.FONT_BUTTON,
            bg="#ff6b6b",
            fg="white",
            activebackground="#ff5252",
            activeforeground="white",
            relief="flat",
            command=excluir
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Salvar",
            font=UI.FONT_BUTTON,
            bg=UI.BTN_BG,
            fg=UI.BTN_FG,
            activebackground=UI.BTN_ACTIVE_BG,
            activeforeground=UI.BTN_ACTIVE_FG,
            relief="flat",
            command=salvar_edicao
        ).pack(side="right", padx=5)

        # Bind do duplo clique
        self.tree.bind("<Double-1>", self._on_item_double_click)

    def _toggle_data_entry(self):
        """Habilita ou desabilita o campo de data de vencimento."""
        if self.tem_vencimento.get():
            self.data_entry.configure(state="normal")
        else:
            self.data_entry.configure(state="disabled")

    def _validar_formulario(self, nome: str, forma: str, data_entry, tem_vencimento, pagamento_id: Optional[int] = None) -> Tuple[bool, Optional[date]]:
        """Valida os campos obrigatórios do formulário e resolve a data opcional.

        Args:
            nome: Nome do método de pagamento
            forma: Forma de pagamento selecionada
            data_entry: Widget DateEntry para obter a data
            tem_vencimento: BooleanVar que indica se há data de vencimento
            pagamento_id: id do pagamento (opcional, usado para editar — ignora o próprio registro)

        Returns:
            (True, date|None) se válido, (False, None) caso contrário
        """
        if not nome:
            self._mostrar_erro("Nome é obrigatório!")
            return False, None
        
        # Verifica nome duplicado (ignora o próprio registro quando editar)
        if self._nome_existe(nome, pagamento_id):
            self._mostrar_erro("Já existe um método de pagamento com esse nome.")
            return False, None

        if not forma:
            self._mostrar_erro("Forma de pagamento é obrigatória!")
            return False, None


        # ÚNICO validador/definição necessária para a data:
        data = data_entry.get_date() if tem_vencimento.get() else None

        return True, data

    def _nome_existe(self, nome: str, ignore_id: Optional[int] = None) -> bool:
        """Verifica se já existe um pagamento com o mesmo nome (case-insensitive).
           Se ignore_id for fornecido, ignora o registro com esse id (útil na edição).
        """
        nome_clean = nome.strip().lower()
        try:
            for p in self.controller.listar_pagamentos():
                pid = getattr(p, "id", None)
                if ignore_id is not None and pid == ignore_id:
                    continue
                if getattr(p, "nome", "").strip().lower() == nome_clean:
                    return True
        except Exception:
            # Em caso de erro ao listar, não considerar como duplicado
            pass
        return False

    def _adicionar_pagamento(self):
        """Adiciona um novo pagamento."""
        nome = self.nome_entry.get().strip()
        forma = self.forma_combo.get()

        valido, data = self._validar_formulario(nome, forma, self.data_entry, self.tem_vencimento)
        if not valido:
            return

        try:
            self.controller.criar_pagamento(
                nome=nome,
                vencimento=data,
                forma_pagamento=FormaPagamento(forma)
            )
            
            # Limpa campos
            self.nome_entry.delete(0, tk.END)
            self.forma_combo.set('')
            self.tem_vencimento.set(False)
            self.data_entry.configure(state="disabled")
            
            # Recarrega dados
            self._load_data()
            
        except Exception as e:
            self._mostrar_erro(str(e))

    def _load_data(self):
        """Carrega os dados na TreeView."""
        # Limpa dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Carrega novos dados
        pagamentos = self.controller.listar_pagamentos()
        for pagamento in pagamentos:
            try:
                # Formata a data apenas se existir
                data_formatada = (
                    pagamento.vencimento.strftime("%d/%m/%Y")
                    if pagamento.vencimento
                    else "Sem vencimento"
                )
                
                values = (
                    getattr(pagamento, 'id', ''),  # ID oculto
                    pagamento.nome,
                    pagamento.forma_de_pagamento.value,
                    data_formatada
                )
                self.tree.insert("", "end", values=values)
            except Exception as e:
                print(f"Erro ao inserir pagamento na TreeView: {str(e)}")
    
    def _mostrar_erro(self, mensagem: str):
        """Método centralizado para exibir mensagens de erro."""
        messagebox.showerror("Erro", mensagem)

