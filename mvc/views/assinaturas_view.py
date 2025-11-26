import tkinter as tk
from tkinter import ttk
from mvc import ui_constants as UI


class AssinaturasView:
    """View para tela de Assinaturas."""
    
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self.assinaturas_data = []
        self.sort_reverse = {}
        self._create_ui()
    
    def _create_ui(self):
        # Título da tela
        title = tk.Label(
            self.parent, 
            text="Assinaturas",
            font=UI.FONT_TITLE,
            bg=UI.BG_COLOR,
            fg="#2e3047"
        )
        title.pack(pady=20)
        
        # Container principal
        main_container = tk.Frame(self.parent, bg=UI.BG_COLOR)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Coluna esquerda
        left_outer = tk.Frame(main_container, bg=UI.BG_COLOR, width=380)
        left_outer.pack(side="left", fill="y", padx=(0, 10), pady=0)
        left_outer.pack_propagate(False)
        
        # Canvas e scrollbar
        canvas_form = tk.Canvas(left_outer, bg=UI.BOX_BG, highlightthickness=0, width=360)
        scrollbar_form = ttk.Scrollbar(left_outer, orient="vertical", command=canvas_form.yview)
        
        left_frame = tk.Frame(canvas_form, bg=UI.BOX_BG, relief="groove", bd=2, width=360)
        
        # Atualiza região de scroll
        def _on_frame_configure(event):
            canvas_form.configure(scrollregion=canvas_form.bbox("all"))
        
        left_frame.bind("<Configure>", _on_frame_configure)
        
        canvas_form.create_window((0, 0), window=left_frame, anchor="nw", width=360)
        canvas_form.configure(yscrollcommand=scrollbar_form.set)
        
        scrollbar_form.pack(side="right", fill="y")
        canvas_form.pack(side="left", fill="both", expand=True)
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas_form.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mousewheel ao entrar
        def _bind_mousewheel(event):
            canvas_form.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel(event):
            canvas_form.unbind_all("<MouseWheel>")
        
        canvas_form.bind("<Enter>", _bind_mousewheel)
        canvas_form.bind("<Leave>", _unbind_mousewheel)
        
        # Coluna direita
        right_frame = tk.Frame(main_container, bg=UI.BG_COLOR)
        right_frame.pack(side="left", fill="both", expand=True, pady=0)
        
        self._create_form(left_frame)
        self._create_treeview(right_frame)
    
    def _create_form(self, parent):
        """Cria o formulário para adicionar assinaturas."""
        form_title = tk.Label(
            parent,
            text="Nova Assinatura",
            font=("Inter", 16, "bold"),
            bg=UI.BOX_BG,
            fg="#2e3047"
        )
        form_title.pack(pady=15, padx=10, fill="x")
        
        # Campo nome
        nome_frame = tk.Frame(parent, bg=UI.BOX_BG)
        nome_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(nome_frame, text="Nome: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(nome_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.entry_nome = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_nome.pack(fill="x", padx=10, pady=(0, 10))
        
        # Campo valor
        valor_frame = tk.Frame(parent, bg=UI.BOX_BG)
        valor_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(valor_frame, text="Valor (R$): ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(valor_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.entry_valor = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_valor.pack(fill="x", padx=10, pady=(0, 10))
        
        # Campo data de vencimento
        data_frame = tk.Frame(parent, bg=UI.BOX_BG)
        data_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(data_frame, text="Vencimento (DD/MM/AAAA): ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(data_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.entry_data = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_data.pack(fill="x", padx=10, pady=(0, 10))
        
        # Campo periodicidade
        period_frame = tk.Frame(parent, bg=UI.BOX_BG)
        period_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(period_frame, text="Periodicidade: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(period_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.combo_periodicidade = ttk.Combobox(parent, font=UI.FONT_ENTRY, state="readonly")
        self.combo_periodicidade.pack(fill="x", padx=10, pady=(0, 10))
        
        # Campo categoria
        categoria_frame = tk.Frame(parent, bg=UI.BOX_BG)
        categoria_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(categoria_frame, text="Categoria: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(categoria_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.combo_categoria = ttk.Combobox(parent, font=UI.FONT_ENTRY, state="readonly")
        self.combo_categoria.pack(fill="x", padx=10, pady=(0, 10))
        
        # Forma de Pagamento
        pag_frame = tk.Frame(parent, bg=UI.BOX_BG)
        pag_frame.pack(anchor="w", padx=10, pady=(5, 0), fill="x")
        tk.Label(pag_frame, text="Forma de Pagamento: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(pag_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        self.combo_pagamento = ttk.Combobox(parent, font=UI.FONT_ENTRY, state="readonly")
        self.combo_pagamento.pack(fill="x", padx=10, pady=(0, 10))
        
        # Usuário Compartilhado
        tk.Label(parent, text="Compartilhado com (email):", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", padx=10, pady=(5, 0))
        self.entry_usuario_compartilhado = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_usuario_compartilhado.pack(fill="x", padx=10, pady=(0, 10))
        
        # Login
        tk.Label(parent, text="Login:", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", padx=10, pady=(5, 0))
        self.entry_login = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_login.pack(fill="x", padx=10, pady=(0, 10))
        
        # Senha
        tk.Label(parent, text="Senha:", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", padx=10, pady=(5, 0))
        self.entry_senha = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG, show="*")
        self.entry_senha.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botão Adicionar
        self.btn_adicionar = tk.Button(
            parent,
            text="Adicionar Assinatura",
            font=UI.FONT_BUTTON,
            bg=UI.BTN_BG,
            fg=UI.BTN_FG,
            activebackground=UI.BTN_ACTIVE_BG,
            activeforeground=UI.BTN_ACTIVE_FG,
            relief="flat",
            command=self._ao_adicionar
        )
        self.btn_adicionar.pack(fill="x", padx=10, pady=20)
    
    def _create_treeview(self, parent):
        """Cria o treeview para exibir as assinaturas."""
        # Frame para o treeview e scrollbars
        tree_container = tk.Frame(parent, bg=UI.BG_COLOR)
        tree_container.pack(fill="both", expand=True)
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_container, orient="vertical")
        scrollbar_x = ttk.Scrollbar(tree_container, orient="horizontal")
        
        # Treeview (ID hidden but stored)
        columns = ("id", "fav", "Nome", "Valor", "Vencimento", "Periodicidade", "Categoria")
        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            height=15,
            displaycolumns=("fav", "Nome", "Valor", "Vencimento", "Periodicidade", "Categoria")
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
        self.tree.heading("fav", text="★", command=lambda: self._ordenar_coluna("fav"))
        self.tree.heading("Nome", text="Nome", command=lambda: self._ordenar_coluna("Nome"))
        self.tree.heading("Valor", text="Valor", command=lambda: self._ordenar_coluna("Valor"))
        self.tree.heading("Vencimento", text="Vencimento", command=lambda: self._ordenar_coluna("Vencimento"))
        self.tree.heading("Periodicidade", text="Periodicidade", command=lambda: self._ordenar_coluna("Periodicidade"))
        self.tree.heading("Categoria", text="Categoria", command=lambda: self._ordenar_coluna("Categoria"))
        
        for col in ("fav", "Nome", "Valor", "Vencimento", "Periodicidade", "Categoria"):
            self.sort_reverse[col] = False
        
        # Larguras das colunas
        self.tree.column("fav", width=40, minwidth=40, anchor="center")
        self.tree.column("Nome", width=150, minwidth=100)
        self.tree.column("Valor", width=100, minwidth=80)
        self.tree.column("Vencimento", width=100, minwidth=80)
        self.tree.column("Periodicidade", width=120, minwidth=100)
        self.tree.column("Categoria", width=120, minwidth=100)
        
        # Bind double-click to show details
        self.tree.bind("<Double-1>", self._on_double_click)
        
        # Bind single click on star column to toggle favorite
        self.tree.bind("<Button-1>", self._on_tree_click)
        
        # Botões
        btn_frame = tk.Frame(parent, bg=UI.BG_COLOR)
        btn_frame.pack(fill="x", pady=10)
        
        # Frame para exibir o total
        total_frame = tk.Frame(parent, bg=UI.BOX_BG, relief="groove", bd=2)
        total_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            total_frame,
            text="Total de Assinaturas:",
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
        
        self.btn_remover = tk.Button(
            btn_frame,
            text="Remover Selecionada",
            font=UI.FONT_BUTTON,
            bg="#ff6b6b",
            fg="#ffffff",
            activebackground="#ff5252",
            activeforeground="#ffffff",
            relief="flat",
            command=self._ao_remover
        )
        self.btn_remover.pack(side="right")
    
    def _on_tree_click(self, event):
        """Handle click on treeview to toggle favorite."""
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
                assinatura_id = values[0]  # ID is hidden but still in values
                if self.controller:
                    self.controller.alternar_favorito(assinatura_id)
    
    def _ordenar_coluna(self, col):
        """Ordena o treeview pela coluna clicada."""
        # Toggle sort direction
        self.sort_reverse[col] = not self.sort_reverse[col]
        reverse = self.sort_reverse[col]
        
        # Sort assinaturas_data
        if col == "fav":
            self.assinaturas_data.sort(
                key=lambda x: x.favorito,
                reverse=not reverse  # Inverted so favorites come first by default
            )
        elif col == "Valor":
            self.assinaturas_data.sort(
                key=lambda x: float(x.valor),
                reverse=reverse
            )
        else:
            attr_map = {
                "Nome": "nome",
                "Vencimento": "data_vencimento",
                "Periodicidade": "periodicidade",
                "Categoria": "categoria"
            }
            attr = attr_map.get(col, "nome")
            self.assinaturas_data.sort(
                key=lambda x: getattr(x, attr, ""),
                reverse=reverse
            )
        
        # Update treeview
        self._atualizar_treeview()
        
        # Update heading to show sort direction
        visible_cols = ("fav", "Nome", "Valor", "Vencimento", "Periodicidade", "Categoria")
        for c in visible_cols:
            if c == col:
                if c == "fav":
                    arrow = " ▼" if not reverse else " ▲"
                    self.tree.heading(c, text="★" + arrow)
                else:
                    arrow = " ▼" if reverse else " ▲"
                    self.tree.heading(c, text=c + arrow)
            else:
                self.tree.heading(c, text="★" if c == "fav" else c)
    
    def _atualizar_treeview(self):
        """Atualiza o treeview com os dados ordenados."""
        # Limpa o treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Re-adiciona as assinaturas
        for assinatura in self.assinaturas_data:
            fav_symbol = "★" if assinatura.favorito == 1 else "☆"
            
            self.tree.insert(
                "",
                "end",
                values=(
                    assinatura.id,  # Hidden but stored
                    fav_symbol,
                    assinatura.nome,
                    f"R$ {assinatura.valor:.2f}",
                    assinatura.data_vencimento,
                    assinatura.periodicidade,
                    assinatura.categoria
                )
            )
        
        # Calcula e atualiza o total usando o controller
        if self.controller:
            total = self.controller.calcular_total_assinaturas(self.assinaturas_data)
            self._atualizar_total(total)
            self._atualizar_diferenca()
    
    def _atualizar_total(self, total: float):
        """Atualiza o label com o valor total das assinaturas."""
        if hasattr(self, 'label_total'):
            self.label_total.config(text=f"R$ {total:.2f}")
    
    def _atualizar_diferenca(self):
        """Atualiza o label com a diferença entre meta e total de assinaturas ativas."""
        if hasattr(self, 'label_diferenca') and self.controller:
            diferenca = self.controller.calcular_diferenca_meta()
            
            # Muda a cor baseado no valor
            if diferenca >= 0:
                cor = "#4CAF50"  # Verde se positivo (dentro da meta)
            else:
                cor = "#ff6b6b"  # Vermelho se negativo (acima da meta)
            
            self.label_diferenca.config(text=f"R$ {diferenca:.2f}", fg=cor)
    
    # O VSCode coloca esse event como não utilizado, mas ele é necessário
    def _on_double_click(self, event):
        """Mostra detalhes completos quando linha é clicada duas vezes."""
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        values = item.get('values')
        if not values:
            return
        
        assinatura_id = values[0]  # ID is first value
        
        # Busca a assinatura
        assinatura = next((a for a in self.assinaturas_data if a.id == assinatura_id), None)
        
        if assinatura:
            self._mostrar_modal_detalhes(assinatura)
    
    def _mostrar_modal_detalhes(self, assinatura):
        """Mostra modal com todos os detalhes da assinatura."""
        modal = tk.Toplevel(self.parent)
        modal.title("Detalhes da Assinatura")
        modal.geometry("500x700")
        modal.configure(bg=UI.BG_COLOR)
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centralizar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (700 // 2)
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
        
        fav_symbol = "★" if assinatura.favorito == 1 else "☆"
        tk.Label(
            title_frame,
            text=fav_symbol,
            font=("Inter", 24),
            bg=UI.BOX_BG,
            fg="#FFD700" if assinatura.favorito == 1 else "#999",
            cursor="hand2"
        ).pack(side="left", padx=(0, 10))
        
        tk.Label(
            title_frame,
            text=assinatura.nome,
            font=("Inter", 20, "bold"),
            bg=UI.BOX_BG,
            fg="#2e3047"
        ).pack(side="left")
        
        # Status com bolinha colorida
        status_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        status_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            status_frame,
            text="Status:",
            font=("Inter", 12, "bold"),
            bg=UI.BOX_BG,
            fg="#2e3047",
            anchor="w"
        ).pack(side="left", padx=(0, 10))
        
        # Determina cor da bolinha baseado no status
        status_value = assinatura.status.value if hasattr(assinatura.status, 'value') else str(assinatura.status)
        status_color = "#4CAF50" if status_value == "Ativo" else "#f44336"
        
        # Canvas para desenhar a bolinha
        status_canvas = tk.Canvas(status_frame, width=16, height=16, bg=UI.BOX_BG, highlightthickness=0)
        status_canvas.create_oval(2, 2, 14, 14, fill=status_color, outline=status_color)
        status_canvas.pack(side="left", padx=(0, 5))
        
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
            ("Nome:", assinatura.nome),
            ("Valor:", f"R$ {assinatura.valor:.2f}"),
            ("Data de Vencimento:", assinatura.data_vencimento),
            ("Periodicidade:", assinatura.periodicidade),
            ("Categoria:", assinatura.categoria),
            ("Forma de Pagamento:", assinatura.forma_pagamento),
            ("Compartilhado com:", assinatura.usuario_compartilhado or "Ninguém"),
            ("Login:", assinatura.login or "N/A"),
            ("Senha:", assinatura.senha or "N/A"),
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
        
        # Se assinatura é readonly (compartilhada), não mostra botão Editar
        if hasattr(assinatura, 'is_readonly') and assinatura.is_readonly:
            # Adiciona indicador de compartilhamento
            tk.Label(
                content_frame,
                text="📌 Assinatura compartilhada (somente leitura)",
                font=("Inter", 10, "italic"),
                bg=UI.BOX_BG,
                fg="#ff9800",
                anchor="w"
            ).pack(pady=(10, 0))
            
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
            ).pack(fill="x")
        else:
            # Assinatura própria - mostra botão Editar
            tk.Button(
                btn_frame,
                text="Editar",
                font=UI.FONT_BUTTON,
                bg="#4CAF50",
                fg="#ffffff",
                activebackground="#45a049",
                activeforeground="#ffffff",
                relief="flat",
                command=lambda: [modal.destroy(), self._mostrar_modal_edicao(assinatura)]
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
    
    def _mostrar_modal_edicao(self, assinatura):
        """Mostra modal para editar uma assinatura."""
        modal = tk.Toplevel(self.parent)
        modal.title("Editar Assinatura")
        modal.geometry("500x700")
        modal.configure(bg=UI.BG_COLOR)
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centralizar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (700 // 2)
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
        
        # Título
        tk.Label(
            content_frame,
            text="Editar Assinatura",
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
        entry_nome.insert(0, assinatura.nome)
        entry_nome.pack(fill="x", pady=(0, 10))
        
        valor_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        valor_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(valor_frame, text="Valor (R$): ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(valor_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        entry_valor = tk.Entry(content_frame, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        entry_valor.insert(0, str(assinatura.valor))
        entry_valor.pack(fill="x", pady=(0, 10))
        
        data_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        data_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(data_frame, text="Vencimento (DD/MM/AAAA): ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(data_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        entry_data = tk.Entry(content_frame, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        entry_data.insert(0, assinatura.data_vencimento)
        entry_data.pack(fill="x", pady=(0, 10))
        
        period_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        period_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(period_frame, text="Periodicidade: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(period_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        combo_periodicidade = ttk.Combobox(content_frame, font=UI.FONT_ENTRY, state="readonly")
        combo_periodicidade['values'] = self.combo_periodicidade['values']
        combo_periodicidade.set(assinatura.periodicidade)
        combo_periodicidade.pack(fill="x", pady=(0, 10))
        
        categoria_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        categoria_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(categoria_frame, text="Categoria: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(categoria_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        combo_categoria = ttk.Combobox(content_frame, font=UI.FONT_ENTRY, state="readonly")
        combo_categoria['values'] = self.combo_categoria['values']
        combo_categoria.set(assinatura.categoria)
        combo_categoria.pack(fill="x", pady=(0, 10))
        
        pag_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        pag_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(pag_frame, text="Forma de Pagamento: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(pag_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        combo_pagamento = ttk.Combobox(content_frame, font=UI.FONT_ENTRY, state="readonly")
        combo_pagamento['values'] = self.combo_pagamento['values']
        combo_pagamento.set(assinatura.forma_pagamento)
        combo_pagamento.pack(fill="x", pady=(0, 10))
        
        tk.Label(content_frame, text="Compartilhado com (email):", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", pady=(5, 0))
        entry_usuario = tk.Entry(content_frame, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        entry_usuario.insert(0, assinatura.usuario_compartilhado or "")
        entry_usuario.pack(fill="x", pady=(0, 10))
        
        tk.Label(content_frame, text="Login:", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", pady=(5, 0))
        entry_login = tk.Entry(content_frame, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        entry_login.insert(0, assinatura.login or "")
        entry_login.pack(fill="x", pady=(0, 10))
        
        tk.Label(content_frame, text="Senha:", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", pady=(5, 0))
        entry_senha = tk.Entry(content_frame, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG, show="*")
        entry_senha.insert(0, assinatura.senha or "")
        entry_senha.pack(fill="x", pady=(0, 10))
        
        # Status
        status_frame = tk.Frame(content_frame, bg=UI.BOX_BG)
        status_frame.pack(anchor="w", pady=(5, 0), fill="x")
        tk.Label(status_frame, text="Status: ", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(side="left")
        tk.Label(status_frame, text="*", font=UI.FONT_LABEL, bg=UI.BOX_BG, fg="#d32f2f").pack(side="left")
        combo_status = ttk.Combobox(content_frame, font=UI.FONT_ENTRY, state="readonly")
        combo_status['values'] = ["Ativo", "Encerrado"]
        status_value = assinatura.status.value if hasattr(assinatura.status, 'value') else str(assinatura.status)
        combo_status.set(status_value)
        combo_status.pack(fill="x", pady=(0, 10))
        
        def salvar_edicao():
            # Coleta dados do modal
            data = {
                'nome': entry_nome.get().strip(),
                'valor': entry_valor.get().strip().replace(',', '.'),
                'data_vencimento': entry_data.get().strip(),
                'periodicidade': combo_periodicidade.get(),
                'categoria': combo_categoria.get(),
                'forma_pagamento': combo_pagamento.get(),
                'usuario_compartilhado': entry_usuario.get().strip(),
                'login': entry_login.get().strip(),
                'senha': entry_senha.get().strip()
            }
            
            # Valida os dados (passa assinatura_id para permitir mesmo nome na edição)
            validacao = self.controller.validar_dados_formulario(data, assinatura_id=assinatura.id)
            
            if not validacao['success']:
                self.controller.mostrar_erro("Erro de Validação", validacao['message'])
                return
            
            validated_data = validacao['data']
            
            # Importa o enum de status
            from mvc.models.status_enum import Status
            
            if self.controller:
                resultado = self.controller.editar(
                    assinatura_id=assinatura.id,
                    nome=validated_data['nome'],
                    data_vencimento=validated_data['data_vencimento'],
                    valor=validated_data['valor'],
                    periodicidade=validated_data['periodicidade'],
                    categoria=validated_data['categoria'],
                    forma_pagamento=validated_data['forma_pagamento'],
                    usuario_compartilhado=validated_data['usuario_compartilhado'],
                    login=validated_data['login'],
                    senha=validated_data['senha'],
                    favorito=assinatura.favorito,
                    status=Status(combo_status.get())
                )
                modal.destroy()
                
                if resultado['success']:
                    self.controller.mostrar_sucesso("Sucesso", resultado['message'])
                else:
                    self.controller.mostrar_erro("Erro no Compartilhamento", resultado['message'])
        
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
    
    def _ao_adicionar(self):
        """Callback quando o botão adicionar é clicado."""
        if self.controller:
            # Obtém dados do formulário via controller
            data = self.controller.obter_dados_formulario()
            
            # Valida os dados (None para nova assinatura)
            validacao = self.controller.validar_dados_formulario(data, assinatura_id=None)
            
            if not validacao['success']:
                # Usa método centralizado para exibir erro
                self.controller.exibir_erro_validacao(validacao)
                return
            
            # Adiciona assinatura
            validated_data = validacao['data']
            resultado = self.controller.adicionar(
                nome=validated_data['nome'],
                data_vencimento=validated_data['data_vencimento'],
                valor=validated_data['valor'],
                periodicidade=validated_data['periodicidade'],
                categoria=validated_data['categoria'],
                forma_pagamento=validated_data['forma_pagamento'],
                usuario_compartilhado=validated_data['usuario_compartilhado'],
                login=validated_data['login'],
                senha=validated_data['senha']
            )
            
            # Verifica resultado
            if resultado['success']:
                # Limpa o formulário
                self.controller.limpar_formulario()
                self.controller.mostrar_sucesso("Sucesso", resultado['message'])
            else:
                self.controller.mostrar_erro("Erro no Compartilhamento", resultado['message'])
    
    def _ao_remover(self):
        """Callback quando o botão remover é clicado."""
        selected = self.tree.selection()
        if not selected:
            self.controller.mostrar_aviso("Aviso", "Selecione uma assinatura para remover!")
            return
        
        item = self.tree.item(selected[0])
        values = item.get('values')
        if values:
            assinatura_id = values[0]
            
            if self.controller:
                if self.controller.confirmar_acao(
                    "Confirmar Remoção",
                    "Deseja realmente remover esta assinatura?\n\nEsta ação não pode ser desfeita."
                ):
                    resultado = self.controller.remover(assinatura_id)
                    
                    if resultado['success']:
                        self.controller.mostrar_sucesso("Sucesso", resultado['message'])
                    else:
                        self.controller.mostrar_erro("Não é possível remover", resultado['message'])
    
    def set_combo_values(self, periodicidades, categorias, formas_pagamento):
        """Define os valores dos comboboxes."""
        self.combo_periodicidade['values'] = periodicidades
        self.combo_categoria['values'] = categorias
        self.combo_pagamento['values'] = formas_pagamento
        
        # Selecionar primeiro item por padrão
        if periodicidades:
            self.combo_periodicidade.current(0)
        if categorias:
            self.combo_categoria.current(0)
        if formas_pagamento:
            self.combo_pagamento.current(0)
    
    def atualizar_lista(self, assinaturas):
        """Atualiza a lista de assinaturas no treeview."""
        # Store full data
        self.assinaturas_data = assinaturas
        
        # Refresh treeview
        self._atualizar_treeview()

