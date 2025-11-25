import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from mvc import ui_constants as UI


class ContratosView:
    """View para tela de Contratos (independente, sem herança de AssinaturasView)."""

    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self.contratos_data = []  # Store full data for sorting
        self.sort_reverse = {}  # Track sort direction per column
        self._create_ui()

    def _create_ui(self):
        # Título
        title = tk.Label(
            self.parent,
            text="Contratos",
            font=UI.FONT_TITLE,
            bg=UI.BG_COLOR,
            fg="#2e3047"
        )
        title.pack(pady=20)

        # Container principal com duas colunas
        main_container = tk.Frame(self.parent, bg=UI.BG_COLOR)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Coluna esquerda - Formulário com scrollbar
        left_outer = tk.Frame(main_container, bg=UI.BG_COLOR, width=380)
        left_outer.pack(side="left", fill="y", padx=(0, 10), pady=0)
        left_outer.pack_propagate(False)

        # Canvas e scrollbar para o formulário
        canvas_form = tk.Canvas(left_outer, bg=UI.BOX_BG, highlightthickness=0, width=360)
        scrollbar_form = ttk.Scrollbar(left_outer, orient="vertical", command=canvas_form.yview)

        left_frame = tk.Frame(canvas_form, bg=UI.BOX_BG, relief="groove", bd=2, width=360)

        # Update scroll region when frame changes
        def _on_frame_configure(event):
            canvas_form.configure(scrollregion=canvas_form.bbox("all"))

        left_frame.bind("<Configure>", _on_frame_configure)

        canvas_form.create_window((0, 0), window=left_frame, anchor="nw", width=360)
        canvas_form.configure(yscrollcommand=scrollbar_form.set)

        scrollbar_form.pack(side="right", fill="y")
        canvas_form.pack(side="left", fill="both", expand=True)

        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas_form.yview_scroll(int(-1*(event.delta/120)), "units")

        # Bind when mouse enters the canvas area
        def _bind_mousewheel(event):
            canvas_form.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_mousewheel(event):
            canvas_form.unbind_all("<MouseWheel>")

        canvas_form.bind("<Enter>", _bind_mousewheel)
        canvas_form.bind("<Leave>", _unbind_mousewheel)

        # Coluna direita - Treeview
        right_frame = tk.Frame(main_container, bg=UI.BG_COLOR)
        right_frame.pack(side="left", fill="both", expand=True, pady=0)

        self._create_form(left_frame)
        self._create_treeview(right_frame)

    def _create_form(self, parent):
        """Cria o formulário para adicionar contratos (sem pagamento, login e senha)."""
        form_title = tk.Label(
            parent,
            text="Novo Contrato",
            font=("Inter", 16, "bold"),
            bg=UI.BOX_BG,
            fg="#2e3047"
        )
        form_title.pack(pady=15, padx=10, fill="x")

        # Nome
        nome_frame = tk.Frame(parent, bg=UI.BOX_BG)
        nome_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(nome_frame, text="Nome: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(nome_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.entry_nome = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_nome.pack(fill="x", padx=10, pady=(0, 10))

        # Valor
        valor_frame = tk.Frame(parent, bg=UI.BOX_BG)
        valor_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(valor_frame, text="Valor (R$): ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(valor_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.entry_valor = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_valor.pack(fill="x", padx=10, pady=(0, 10))

        # Data de Vencimento
        data_frame = tk.Frame(parent, bg=UI.BOX_BG)
        data_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(data_frame, text="Vencimento (DD/MM/AAAA): ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(data_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.entry_data = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_data.pack(fill="x", padx=10, pady=(0, 10))

        # Periodicidade
        period_frame = tk.Frame(parent, bg=UI.BOX_BG)
        period_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(period_frame, text="Periodicidade: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(period_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.combo_periodicidade = ttk.Combobox(parent, font=UI.FONT_ENTRY, state="readonly")
        self.combo_periodicidade.pack(fill="x", padx=10, pady=(0, 10))

        categoria_frame = tk.Frame(parent, bg=UI.BOX_BG)
        categoria_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(categoria_frame, text="Categoria: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(categoria_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.combo_categoria = ttk.Combobox(parent, font=UI.FONT_ENTRY, state="readonly")
        self.combo_categoria.pack(fill="x", padx=10, pady=(0, 10))

        # Forma de Pagamento (obrigatório)
        pagamento_frame = tk.Frame(parent, bg=UI.BOX_BG)
        pagamento_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(pagamento_frame, text="Forma de Pagamento: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(pagamento_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.combo_forma_pagamento = ttk.Combobox(parent, font=UI.FONT_ENTRY, state="readonly")
        self.combo_forma_pagamento.pack(fill="x", padx=10, pady=(0, 10))

        # Usuário Compartilhado (opcional)
        compartilhado_frame = tk.Frame(parent, bg=UI.BOX_BG)
        compartilhado_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(compartilhado_frame, text="Compartilhar com (email): ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        self.entry_usuario_compartilhado = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_usuario_compartilhado.pack(fill="x", padx=10, pady=(0, 10))

        # Botão Adicionar
        self.btn_adicionar = tk.Button(
            parent,
            text="Adicionar Contrato",
            font=UI.FONT_BUTTON,
            bg=UI.BTN_BG,
            fg=UI.BTN_FG,
            activebackground=UI.BTN_ACTIVE_BG,
            activeforeground=UI.BTN_ACTIVE_FG,
            relief="flat",
            command=self._on_adicionar
        )
        self.btn_adicionar.pack(fill="x", padx=10, pady=20)

    def set_combo_values(self, periodicidades, categorias, formas_pagamento):
        """Define os valores dos comboboxes (com formas de pagamento)."""
        self.combo_periodicidade['values'] = periodicidades
        self.combo_categoria['values'] = categorias
        self.combo_forma_pagamento['values'] = formas_pagamento

        # Selecionar primeiro item por padrão
        if periodicidades:
            self.combo_periodicidade.current(0)
        if categorias:
            self.combo_categoria.current(0)
        if formas_pagamento:
            self.combo_forma_pagamento.current(0)

    def _create_treeview(self, parent):
        """Cria o treeview para exibir os contratos."""
        # Frame para o treeview e scrollbars
        tree_container = tk.Frame(parent, bg=UI.BG_COLOR)
        tree_container.pack(fill="both", expand=True)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_container, orient="vertical")
        scrollbar_x = ttk.Scrollbar(tree_container, orient="horizontal")

        # Treeview (ID hidden but stored) - ADICIONADO Status
        columns = ("id", "fav", "Nome", "Valor", "Vencimento", "Periodicidade", "Categoria", "Status")
        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            height=15,
            displaycolumns=("fav", "Nome", "Valor", "Vencimento", "Periodicidade", "Categoria", "Status")
        )

        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # Posicionar scrollbars e treeview
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Definir colunas com comando de ordenação
        self.tree.heading("fav", text="★", command=lambda: self._sort_column("fav"))
        self.tree.heading("Nome", text="Nome", command=lambda: self._sort_column("Nome"))
        self.tree.heading("Valor", text="Valor", command=lambda: self._sort_column("Valor"))
        self.tree.heading("Vencimento", text="Vencimento", command=lambda: self._sort_column("Vencimento"))
        self.tree.heading("Periodicidade", text="Periodicidade", command=lambda: self._sort_column("Periodicidade"))
        self.tree.heading("Categoria", text="Categoria", command=lambda: self._sort_column("Categoria"))
        self.tree.heading("Status", text="Status", command=lambda: self._sort_column("Status"))

        # Inicializar dicionário de ordenação
        self.sort_reverse = {}
        for col in ("fav", "Nome", "Valor", "Vencimento", "Periodicidade", "Categoria", "Status"):
            self.sort_reverse[col] = False

        # Larguras das colunas
        self.tree.column("fav", width=40, minwidth=40, anchor="center")
        self.tree.column("Nome", width=120, minwidth=100)
        self.tree.column("Valor", width=100, minwidth=80)
        self.tree.column("Vencimento", width=100, minwidth=80)
        self.tree.column("Periodicidade", width=100, minwidth=90)
        self.tree.column("Categoria", width=100, minwidth=90)
        self.tree.column("Status", width=80, minwidth=70, anchor="center")

        # Bind double-click to show details
        self.tree.bind("<Double-1>", self._on_double_click)
        
        # Bind single click on star column to toggle favorite
        self.tree.bind("<Button-1>", self._on_tree_click)

        # Botões - MOVIDO PARA CIMA DO TOTAL
        btn_frame = tk.Frame(parent, bg=UI.BG_COLOR)
        btn_frame.pack(fill="x", pady=10)
        
        self.btn_remover = tk.Button(
            btn_frame,
            text="Remover Selecionado",
            font=UI.FONT_BUTTON,
            bg="#ff6b6b",
            fg="#ffffff",
            activebackground="#ff5252",
            activeforeground="#ffffff",
            relief="flat",
            command=self._on_remover
        )
        self.btn_remover.pack(side="right")

        # Frame para exibir o total
        total_frame = tk.Frame(parent, bg=UI.BOX_BG, relief="groove", bd=2)
        total_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            total_frame,
            text="Total de Contratos:",
            font=("Inter", 12, "bold"),
            bg=UI.BOX_BG,
            fg="#2e3047"
        ).pack(side="left", padx=15, pady=10)
        
        self.label_total = tk.Label(
            total_frame,
            text="R$ 0,00",
            font=("Inter", 14, "bold"),
            bg=UI.BOX_BG,
            fg="#4CAF50"
        )
        self.label_total.pack(side="right", padx=15, pady=10)
        
        # Frame para exibir a diferença (Meta - Total)
        diferenca_frame = tk.Frame(parent, bg=UI.BOX_BG, relief="groove", bd=2)
        diferenca_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            diferenca_frame,
            text="Disponível (Meta - Total):",
            font=("Inter", 12, "bold"),
            bg=UI.BOX_BG,
            fg="#2e3047"
        ).pack(side="left", padx=15, pady=10)
        
        self.label_diferenca = tk.Label(
            diferenca_frame,
            text="R$ 0,00",
            font=("Inter", 14, "bold"),
            bg=UI.BOX_BG,
            fg="#2196F3"
        )
        self.label_diferenca.pack(side="right", padx=15, pady=10)

    def _refresh_treeview(self):
        """Atualiza o treeview com os dados ordenados."""
        # Limpa o treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Re-adiciona os contratos
        for contrato in self.contratos_data:
            fav_symbol = "★" if contrato.favorito == 1 else "☆"
            status_value = contrato.status.value if hasattr(contrato.status, 'value') else contrato.status

            self.tree.insert(
                "",
                "end",
                values=(
                    contrato.id,
                    fav_symbol,
                    contrato.nome,
                    f"R$ {contrato.valor:.2f}",
                    contrato.data_vencimento,
                    contrato.periodicidade,
                    contrato.categoria,  # Categoria do contrato
                    status_value
                )
            )

        # Calcula e atualiza o total usando o controller
        if self.controller:
            total = self.controller.calcular_total_contratos(self.contratos_data)
            self._atualizar_total(total)
            self._atualizar_diferenca()

    def _atualizar_total(self, total: float):
        """Atualiza o label com o valor total dos contratos."""
        if hasattr(self, 'label_total'):
            self.label_total.config(text=f"R$ {total:.2f}")
    
    def _atualizar_diferenca(self):
        """Atualiza o label com a diferença entre meta e total de contratos ativos."""
        if hasattr(self, 'label_diferenca') and self.controller:
            diferenca = self.controller.calcular_diferenca_meta()
            
            # Muda a cor baseado no valor
            if diferenca >= 0:
                cor = "#4CAF50"  # Verde se positivo (dentro da meta)
            else:
                cor = "#ff6b6b"  # Vermelho se negativo (acima da meta)
            
            self.label_diferenca.config(text=f"R$ {diferenca:.2f}", fg=cor)

    def _on_adicionar(self):
        """Callback quando o botão adicionar é clicado (com validação)."""
        if self.controller:
            # Obtém dados do formulário via controller
            data = self.controller.get_form_data()
            
            # Valida os dados (None para novo contrato)
            validation = self.controller.validate_form_data(data, contrato_id=None)
            
            if not validation['success']:
                # Usa método centralizado para exibir erro
                self.controller.exibir_erro_validacao(validation)
                return
            
            # Adiciona contrato
            validated_data = validation['data']
            resultado = self.controller.adicionar(
                nome=validated_data['nome'],
                data_vencimento=validated_data['data_vencimento'],
                valor=validated_data['valor'],
                periodicidade=validated_data['periodicidade'],
                categoria=validated_data['categoria'],  # Categoria do contrato
                forma_pagamento=validated_data.get('forma_pagamento', ''),
                usuario_compartilhado=validated_data['usuario_compartilhado']
            )
            
            # Verifica resultado
            if resultado['success']:
                # Limpa o formulário
                self.controller.clear_form()
                self.controller.mostrar_sucesso("Sucesso", resultado['message'])
            else:
                self.controller.mostrar_erro("Erro", resultado['message'])

    def _on_remover(self):
        """Callback quando o botão remover é clicado (com validação de status)."""
        selected = self.tree.selection()
        if not selected:
            self.controller.mostrar_aviso("Aviso", "Selecione um contrato para remover!")
            return
        
        item = self.tree.item(selected[0])
        values = item.get('values')
        if values:
            contrato_id = values[0]
            
            if self.controller:
                if self.controller.confirmar_acao(
                    "Confirmar Remoção",
                    "Deseja realmente remover este contrato?\n\nEsta ação não pode ser desfeita."
                ):
                    resultado = self.controller.remover(contrato_id)
                    
                    if resultado['success']:
                        self.controller.mostrar_sucesso("Sucesso", resultado['message'])
                    else:
                        self.controller.mostrar_erro("Não é possível remover", resultado['message'])

    def _show_detail_modal(self, contrato):
        """Mostra modal com todos os detalhes do contrato."""
        modal = tk.Toplevel(self.parent)
        modal.title("Detalhes do Contrato")
        modal.geometry("500x600")
        modal.configure(bg=UI.BG_COLOR)
        modal.transient(self.parent)
        modal.grab_set()

        # Centralizar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (600 // 2)
        modal.geometry(f"+{x}+{y}")

        # Container com scroll
        canvas = tk.Canvas(modal, bg=UI.BOX_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(modal, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg=UI.BOX_BG, padx=30, pady=30)

        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Título com favorito
        title_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        title_frame.pack(pady=(0, 10))

        fav_symbol = "★" if contrato.favorito == 1 else "☆"
        tk.Label(
            title_frame,
            text=fav_symbol,
            font=("Inter", 24),
            bg=UI.BOX_BG,
            fg="#FFD700" if contrato.favorito == 1 else "#999",
            cursor="hand2"
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            title_frame,
            text=contrato.nome,
            font=("Inter", 20, "bold"),
            bg=UI.BOX_BG,
            fg="#2e3047"
        ).pack(side="left")

        # Status com bolinha colorida
        status_value = contrato.status.value if hasattr(contrato.status, 'value') else contrato.status
        status_color = "#4CAF50" if status_value == "Ativo" else "#F44336"

        status_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        status_frame.pack(fill="x", pady=10)

        tk.Label(
            status_frame,
            text="Status:",
            font=("Inter", 12, "bold"),
            bg=UI.BOX_BG,
            fg="#2e3047",
            anchor="w"
        ).pack(side="left", padx=(0, 10))

        # Bolinha colorida
        tk.Label(
            status_frame,
            text="●",
            font=("Inter", 16),
            bg=UI.BOX_BG,
            fg=status_color,
            anchor="w"
        ).pack(side="left", padx=(0, 5))

        tk.Label(
            status_frame,
            text=status_value,
            font=("Inter", 12),
            bg=UI.BOX_BG,
            fg="#555",
            anchor="w"
        ).pack(side="left")

        # Detalhes
        details = [
            ("Nome:", contrato.nome),
            ("Valor:", f"R$ {contrato.valor:.2f}"),
            ("Data de Vencimento:", contrato.data_vencimento),
            ("Periodicidade:", contrato.periodicidade),
            ("Categoria:", contrato.categoria),  # Categoria do contrato
        ]

        for label, value in details:
            frame = tk.Frame(content_frame, bg=UI.BOX_BG)
            frame.pack(fill="x", pady=5)

            tk.Label(
                frame,
                text=label,
                font=("Inter", 12, "bold"),
                bg=UI.BOX_BG,
                fg="#2e3047",
                anchor="w"
            ).pack(side="left", padx=(0, 10))

            tk.Label(
                frame,
                text=value,
                font=("Inter", 12),
                bg=UI.BOX_BG,
                fg="#555",
                anchor="w"
            ).pack(side="left", fill="x", expand=True)

        # Botões
        btn_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        btn_frame.pack(pady=(30, 0), fill="x")
        
        # Todos os contratos podem ser editados (compartilhamento removido)
        tk.Button(
            btn_frame,
            text="Editar",
            font=UI.FONT_BUTTON,
            bg="#4CAF50",
            fg="#ffffff",
            activebackground="#45a049",
            activeforeground="#ffffff",
            relief="flat",
            command=lambda: [modal.destroy(), self._show_edit_modal(contrato)]
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Button(
            btn_frame,
            text="Fechar",
            font=UI.FONT_BUTTON,
            bg=UI.BTN_BG,
            fg=UI.BTN_FG,
            activebackground=UI.BTN_ACTIVE_BG,
            activeforeground=UI.BTN_ACTIVE_FG,
            relief="flat",
            command=modal.destroy
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def _show_edit_modal(self, contrato):
        """Mostra modal para editar um contrato (com validação)."""
        modal = tk.Toplevel(self.parent)
        modal.title("Editar Contrato")
        modal.configure(bg=UI.BOX_BG)
        modal.geometry("600x600")

        # Centralizar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (600 // 2)
        y = (modal.winfo_screenheight() // 2) - (600 // 2)
        modal.geometry(f"+{x}+{y}")

        content_frame = tk.Frame(modal, bg=UI.BOX_BG)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        tk.Label(
            content_frame,
            text="Editar Contrato",
            font=("Inter", 18, "bold"),
            bg=UI.BOX_BG,
            fg="#2e3047"
        ).pack(pady=(0, 20))

        # Campos do formulário
        nome_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        nome_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(nome_frame, text="Nome: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(nome_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        entry_nome = tk.Entry(content_frame, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        entry_nome.insert(0, contrato.nome)
        entry_nome.pack(fill="x", pady=(0, 10))

        valor_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        valor_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(valor_frame, text="Valor (R$): ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(valor_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        entry_valor = tk.Entry(content_frame, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        entry_valor.insert(0, str(contrato.valor))
        entry_valor.pack(fill="x", pady=(0, 10))

        data_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        data_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(data_frame, text="Vencimento (DD/MM/AAAA): ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(data_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        entry_data = tk.Entry(content_frame, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        entry_data.insert(0, contrato.data_vencimento)
        entry_data.pack(fill="x", pady=(0, 10))

        period_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        period_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(period_frame, text="Periodicidade: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(period_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        combo_periodicidade = ttk.Combobox(content_frame, font=UI.FONT_ENTRY, state="readonly")
        combo_periodicidade['values'] = self.combo_periodicidade['values']
        combo_periodicidade.set(contrato.periodicidade)
        combo_periodicidade.pack(fill="x", pady=(0, 10))

        categoria_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        categoria_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(categoria_frame, text="Categoria: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(categoria_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        combo_categoria = ttk.Combobox(content_frame, font=UI.FONT_ENTRY, state="readonly")
        combo_categoria['values'] = self.combo_categoria['values']
        combo_categoria.set(contrato.categoria)  # Categoria do contrato
        combo_categoria.pack(fill="x", pady=(0, 10))

        # Forma de Pagamento (obrigatório)
        pagamento_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        pagamento_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(pagamento_frame, text="Forma de Pagamento: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(pagamento_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        combo_forma_pagamento = ttk.Combobox(content_frame, font=UI.FONT_ENTRY, state="readonly")
        combo_forma_pagamento['values'] = self.combo_forma_pagamento['values']
        combo_forma_pagamento.set(contrato.forma_pagamento or "")
        combo_forma_pagamento.pack(fill="x", pady=(0, 10))

        # Usuário Compartilhado (opcional)
        compartilhado_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        compartilhado_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(compartilhado_frame, text="Compartilhar com (email): ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        entry_usuario_compartilhado = tk.Entry(content_frame, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        entry_usuario_compartilhado.insert(0, contrato.usuario_compartilhado or "")
        entry_usuario_compartilhado.pack(fill="x", pady=(0, 10))

        # Status
        status_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        status_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(status_frame, text="Status: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(status_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        combo_status = ttk.Combobox(content_frame, font=UI.FONT_ENTRY, state="readonly")
        combo_status['values'] = ["Ativo", "Encerrado"]
        status_value = contrato.status.value if hasattr(contrato.status, 'value') else str(contrato.status)
        combo_status.set(status_value)
        combo_status.pack(fill="x", pady=(0, 10))

        def salvar_edicao():
            # Coleta dados do modal
            data = {
                'nome': entry_nome.get().strip(),
                'valor': entry_valor.get().strip().replace(',', '.'),
                'data_vencimento': entry_data.get().strip(),
                'periodicidade': combo_periodicidade.get(),
                'categoria': combo_categoria.get(),  # Categoria do contrato
                'forma_pagamento': combo_forma_pagamento.get(),
                'usuario_compartilhado': entry_usuario_compartilhado.get().strip()
            }
            
            # Valida os dados (passa contrato_id para permitir mesmo nome na edição)
            validation = self.controller.validate_form_data(data, contrato_id=contrato.id)
            
            if not validation['success']:
                self.controller.exibir_erro_validacao(validation)
                return
            
            validated_data = validation['data']
            
            # Importa o enum de status
            from mvc.models.status_enum import Status
            
            if self.controller:
                resultado = self.controller.editar(
                    contrato_id=contrato.id,
                    nome=validated_data['nome'],
                    data_vencimento=validated_data['data_vencimento'],
                    valor=validated_data['valor'],
                    periodicidade=validated_data['periodicidade'],
                    categoria=validated_data['categoria'],  # Categoria do contrato
                    forma_pagamento=validated_data.get('forma_pagamento', ''),
                    usuario_compartilhado=validated_data['usuario_compartilhado'],
                    favorito=contrato.favorito,
                    status=Status(combo_status.get())
                )
                modal.destroy()
                
                if resultado['success']:
                    self.controller.mostrar_sucesso("Sucesso", resultado['message'])
                else:
                    self.controller.mostrar_erro("Erro", resultado['message'])
        
        # Botões
        btn_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        btn_frame.pack(pady=(20, 0), fill="x")
        
        tk.Button(
            btn_frame,
            text="Salvar",
            font=UI.FONT_BUTTON,
            bg="#4CAF50",
            fg="#ffffff",
            activebackground="#45a049",
            activeforeground="#ffffff",
            relief="flat",
            command=salvar_edicao
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            font=UI.FONT_BUTTON,
            bg="#ff6b6b",
            fg="#ffffff",
            activebackground="#ff5252",
            activeforeground="#ffffff",
            relief="flat",
            command=modal.destroy
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def _on_double_click(self, event):
        """Callback quando há double click no treeview."""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item.get('values')
            if values and len(values) >= 7:  # Verifica se tem dados suficientes
                contrato_id = values[0]
                
                # Encontra o contrato nos dados
                for contrato in self.contratos_data:
                    if str(contrato.id) == str(contrato_id):
                        self._show_detail_modal(contrato)
                        break
    
    def _on_tree_click(self, event):
        """Callback quando há click no treeview para toggle favorito."""
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            return
        
        column = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)
        
        # Check if click was on favorite column (#1 = fav column)
        if column == "#1" and row_id:
            item = self.tree.item(row_id)
            values = item.get('values')
            if values:
                contrato_id = values[0]  # ID is hidden but still in values
                if self.controller:
                    self.controller.toggle_favorito(contrato_id)
    
    def atualizar_lista(self, contratos):
        """Atualiza a lista de contratos no treeview."""
        # Store full data
        self.contratos_data = contratos
        
        # Refresh treeview
        self._refresh_treeview()