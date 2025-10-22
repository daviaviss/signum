import tkinter as tk
from tkinter import ttk, messagebox
from mvc import ui_constants as UI


class AssinaturasView:
    """View para tela de Assinaturas."""
    
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
        self.assinaturas_data = []  # Store full data for sorting
        self.sort_reverse = {}  # Track sort direction per column
        self._create_ui()
    
    def _create_ui(self):
        # Título
        title = tk.Label(
            self.parent, 
            text="Assinaturas",
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
        """Cria o formulário para adicionar assinaturas."""
        form_title = tk.Label(
            parent,
            text="Nova Assinatura",
            font=("Inter", 16, "bold"),
            bg=UI.BOX_BG,
            fg="#2e3047"
        )
        form_title.pack(pady=15, padx=10, fill="x")
        
        # Nome
        tk.Label(parent, text="Nome:", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", padx=10, pady=(5, 0))
        self.entry_nome = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_nome.pack(fill="x", padx=10, pady=(0, 10))
        
        # Valor
        tk.Label(parent, text="Valor (R$):", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", padx=10, pady=(5, 0))
        self.entry_valor = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_valor.pack(fill="x", padx=10, pady=(0, 10))
        
        # Data de Vencimento
        tk.Label(parent, text="Vencimento (DD/MM/AAAA):", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", padx=10, pady=(5, 0))
        self.entry_data = tk.Entry(parent, font=UI.FONT_ENTRY, bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.entry_data.pack(fill="x", padx=10, pady=(0, 10))
        
        # Periodicidade
        tk.Label(parent, text="Periodicidade:", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", padx=10, pady=(5, 0))
        self.combo_periodicidade = ttk.Combobox(parent, font=UI.FONT_ENTRY, state="readonly")
        self.combo_periodicidade.pack(fill="x", padx=10, pady=(0, 10))
        
        # Tag
        tk.Label(parent, text="Categoria:", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", padx=10, pady=(5, 0))
        self.combo_tag = ttk.Combobox(parent, font=UI.FONT_ENTRY, state="readonly")
        self.combo_tag.pack(fill="x", padx=10, pady=(0, 10))
        
        # Forma de Pagamento
        tk.Label(parent, text="Forma de Pagamento:", font=UI.FONT_LABEL, bg=UI.BOX_BG).pack(anchor="w", padx=10, pady=(5, 0))
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
            command=self._on_adicionar
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
        self.tree.heading("fav", text="★", command=lambda: self._sort_column("fav"))
        self.tree.heading("Nome", text="Nome", command=lambda: self._sort_column("Nome"))
        self.tree.heading("Valor", text="Valor", command=lambda: self._sort_column("Valor"))
        self.tree.heading("Vencimento", text="Vencimento", command=lambda: self._sort_column("Vencimento"))
        self.tree.heading("Periodicidade", text="Periodicidade", command=lambda: self._sort_column("Periodicidade"))
        self.tree.heading("Categoria", text="Categoria", command=lambda: self._sort_column("Categoria"))
        
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
        
        self.btn_remover = tk.Button(
            btn_frame,
            text="Remover Selecionada",
            font=UI.FONT_BUTTON,
            bg="#ff6b6b",
            fg="#ffffff",
            activebackground="#ff5252",
            activeforeground="#ffffff",
            relief="flat",
            command=self._on_remover
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
                    self.controller.toggle_favorito(assinatura_id)
    
    def _sort_column(self, col):
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
                "Categoria": "tag"
            }
            attr = attr_map.get(col, "nome")
            self.assinaturas_data.sort(
                key=lambda x: getattr(x, attr, ""),
                reverse=reverse
            )
        
        # Update treeview
        self._refresh_treeview()
        
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
    
    def _refresh_treeview(self):
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
                    assinatura.tag
                )
            )
    
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
        
        # Encontra a assinatura completa
        assinatura = next((a for a in self.assinaturas_data if a.id == assinatura_id), None)
        if assinatura:
            self._show_detail_modal(assinatura)
    
    def _show_detail_modal(self, assinatura):
        """Mostra modal com todos os detalhes da assinatura."""
        modal = tk.Toplevel(self.parent)
        modal.title("Detalhes da Assinatura")
        modal.geometry("500x650")
        modal.configure(bg=UI.BG_COLOR)
        modal.transient(self.parent)
        modal.grab_set()
        
        # Centralizar modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (650 // 2)
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
        
        # Detalhes
        details = [
            ("Nome:", assinatura.nome),
            ("Valor:", f"R$ {assinatura.valor:.2f}"),
            ("Data de Vencimento:", assinatura.data_vencimento),
            ("Periodicidade:", assinatura.periodicidade),
            ("Categoria:", assinatura.tag),
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
        
        # Botão fechar
        tk.Button(
            content_frame,
            text="Fechar",
            font=UI.FONT_BUTTON,
            bg=UI.BTN_BG,
            fg=UI.BTN_FG,
            activebackground=UI.BTN_ACTIVE_BG,
            activeforeground=UI.BTN_ACTIVE_FG,
            relief="flat",
            command=modal.destroy
        ).pack(pady=(30, 0), fill="x")
    
    def _on_adicionar(self):
        """Callback quando o botão adicionar é clicado."""
        if self.controller:
            try:
                nome = self.entry_nome.get().strip()
                valor = float(self.entry_valor.get().strip().replace(",", "."))
                data = self.entry_data.get().strip()
                periodicidade = self.combo_periodicidade.get()
                tag = self.combo_tag.get()
                pagamento = self.combo_pagamento.get()
                usuario_compartilhado = self.entry_usuario_compartilhado.get().strip()
                login = self.entry_login.get().strip()
                senha = self.entry_senha.get().strip()
                
                if not nome or not data or not periodicidade or not tag or not pagamento:
                    messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                    return
                
                self.controller.adicionar(
                    nome=nome,
                    data_vencimento=data,
                    valor=valor,
                    periodicidade=periodicidade,
                    tag=tag,
                    forma_pagamento=pagamento,
                    usuario_compartilhado=usuario_compartilhado,
                    login=login,
                    senha=senha
                )
                
                # Limpar campos
                self.entry_nome.delete(0, tk.END)
                self.entry_valor.delete(0, tk.END)
                self.entry_data.delete(0, tk.END)
                self.entry_usuario_compartilhado.delete(0, tk.END)
                self.entry_login.delete(0, tk.END)
                self.entry_senha.delete(0, tk.END)
                
                messagebox.showinfo("Sucesso", "Assinatura adicionada com sucesso!")
                
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido! Use apenas números.")
    
    def _on_remover(self):
        """Callback quando o botão remover é clicado."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma assinatura para remover!")
            return
        
        item = self.tree.item(selected[0])
        values = item.get('values')
        if values:
            assinatura_id = values[0]
            
            if self.controller:
                confirm = messagebox.askyesno("Confirmar", "Deseja realmente remover esta assinatura?")
                if confirm:
                    self.controller.remover(assinatura_id)
                    messagebox.showinfo("Sucesso", "Assinatura removida com sucesso!")
    
    def set_combo_values(self, periodicidades, tags, formas_pagamento):
        """Define os valores dos comboboxes."""
        self.combo_periodicidade['values'] = periodicidades
        self.combo_tag['values'] = tags
        self.combo_pagamento['values'] = formas_pagamento
        
        # Selecionar primeiro item por padrão
        if periodicidades:
            self.combo_periodicidade.current(0)
        if tags:
            self.combo_tag.current(0)
        if formas_pagamento:
            self.combo_pagamento.current(0)
    
    def atualizar_lista(self, assinaturas):
        """Atualiza a lista de assinaturas no treeview."""
        # Store full data
        self.assinaturas_data = assinaturas
        
        # Refresh treeview
        self._refresh_treeview()
