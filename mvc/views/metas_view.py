# mvc/views/metas_view.py
import tkinter as tk
from tkinter import messagebox, PhotoImage
from mvc import ui_constants as UI


class MetasView:
    """
    View de conteúdo para a tela 'Metas'.
    - NÃO cria o navbar (controlado pela UserLoginView).
    - Usa os padrões de estilo definidos em ui_constants.py.
    - Integra com o usuario_controller (opcional) para atualizar limites.
    """

    # Fator de redução do círculo (2 = metade, 3 = 1/3, etc.)
    CIRCLE_SUBSAMPLE = 2

    # Larguras mais contidas para inputs e botões
    ENTRY_WIDTH = 14
    BUTTON_WIDTH = 16
    BUTTON_HEIGHT = 1

    def __init__(self, parent: tk.Widget, usuario_controller=None):
        self.parent = parent
        self.usuario_controller = usuario_controller

        # Frame raiz do conteúdo
        self.frame = tk.Frame(self.parent, bg=UI.BG_COLOR)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Cria os dois cards (Assinaturas / Contratos)
        self._build_cards()

    # ---------------- FORMATADORES ----------------
    def _format_brl(self, valor: float) -> str:
        """R$9.999,99"""
        s = f"{abs(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{'-' if valor < 0 else ''}R${s}"

    def _format_display(self, valor: float) -> str:
        """
        Exibe abreviado:
          - >= 10.000: 'R$10mil', 'R$10,5mil', ...
          - >= 1.000.000: 'R$1,2M'
          - abaixo de 10.000: BRL normal (R$9.999,99)
        """
        sign = "-" if valor < 0 else ""
        v = abs(float(valor))

        if v >= 1_000_000:
            n = v / 1_000_000
            # 1 casa decimal se necessário (1,2M), senão inteiro (2M)
            num = f"{n:.1f}" if n % 1 else f"{int(n)}"
            num = num.replace(".", ",")
            return f"{sign}R${num}M"

        if v >= 10_000:
            n = v / 1_000
            num = f"{n:.1f}" if n % 1 else f"{int(n)}"
            num = num.replace(".", ",")
            return f"{sign}R${num}mil"

        # para valores menores, formato BRL completo
        return f"{sign}{self._format_brl(v)}"

    # ---------------- UI BUILD ----------------
    def _build_cards(self):
        """Monta a interface dos dois cards principais (Assinaturas / Contratos)."""

        # ==== CARD ASSINATURAS ====
        frame_ass = tk.Frame(self.frame, bg=UI.BOX_CARD_BG, bd=2,
                             relief="groove", padx=20, pady=20)
        frame_ass.pack(side="left", expand=True, padx=20)

        tk.Label(frame_ass, text="Assinaturas", font=("Arial", 12, "bold"),
                 bg=UI.BOX_CARD_BG).pack(pady=(0, 12))

        # Círculo reduzido (sem Pillow)
        self.circle_ass = PhotoImage(file="static/circle.png").subsample(
            self.CIRCLE_SUBSAMPLE, self.CIRCLE_SUBSAMPLE
        )
        circle_label_ass = tk.Label(frame_ass, image=self.circle_ass, bg=UI.BOX_CARD_BG)
        circle_label_ass.pack()

        # Texto central dentro do círculo
        val_ass = self._valor_inicial("assinaturas")
        self.label_ass = tk.Label(
            frame_ass,
            text=self._format_display(val_ass),
            font=("Arial", 14, "bold"),
            bg=UI.BOX_CARD_BG
        )
        self.label_ass.place(in_=circle_label_ass, relx=0.5, rely=0.5, anchor="center")

        # Campo de entrada
        self.entry_ass = tk.Entry(
            frame_ass,
            justify="center",
            width=self.ENTRY_WIDTH,
            font=UI.FONT_ENTRY,
            bg=UI.ENTRY_BG,
            fg=UI.ENTRY_FG,
            insertbackground=UI.ENTRY_CURSOR_COLOR
        )
        self.entry_ass.pack(pady=8)

        # Botão salvar
        btn_ass = tk.Button(
            frame_ass,
            text="Cadastrar novo limite",
            command=self._salvar_limite_ass,
            bg=UI.BTN_BG,
            fg=UI.BTN_FG,
            activebackground=UI.BTN_ACTIVE_BG,
            activeforeground=UI.BTN_ACTIVE_FG,
            font=UI.FONT_BUTTON,
            relief="flat",
            borderwidth=0,
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT
        )
        btn_ass.pack()

        # ==== CARD CONTRATOS ====
        frame_con = tk.Frame(self.frame, bg=UI.BOX_CARD_BG, bd=2,
                             relief="groove", padx=20, pady=20)
        frame_con.pack(side="right", expand=True, padx=20)

        tk.Label(frame_con, text="Contratos", font=("Arial", 12, "bold"),
                 bg=UI.BOX_CARD_BG).pack(pady=(0, 12))

        self.circle_con = PhotoImage(file="static/circle.png").subsample(
            self.CIRCLE_SUBSAMPLE, self.CIRCLE_SUBSAMPLE
        )
        circle_label_con = tk.Label(frame_con, image=self.circle_con, bg=UI.BOX_CARD_BG)
        circle_label_con.pack()

        val_con = self._valor_inicial("contratos")
        self.label_con = tk.Label(
            frame_con,
            text=self._format_display(val_con),
            font=("Arial", 14, "bold"),
            bg=UI.BOX_CARD_BG
        )
        self.label_con.place(in_=circle_label_con, relx=0.5, rely=0.5, anchor="center")

        self.entry_con = tk.Entry(
            frame_con,
            justify="center",
            width=self.ENTRY_WIDTH,
            font=UI.FONT_ENTRY,
            bg=UI.ENTRY_BG,
            fg=UI.ENTRY_FG,
            insertbackground=UI.ENTRY_CURSOR_COLOR
        )
        self.entry_con.pack(pady=8)

        btn_con = tk.Button(
            frame_con,
            text="Cadastrar novo limite",
            command=self._salvar_limite_con,
            bg=UI.BTN_BG,
            fg=UI.BTN_FG,
            activebackground=UI.BTN_ACTIVE_BG,
            activeforeground=UI.BTN_ACTIVE_FG,
            font=UI.FONT_BUTTON,
            relief="flat",
            borderwidth=0,
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT
        )
        btn_con.pack()

    # ---------------- HELPERS ----------------
    def _valor_inicial(self, tipo: str) -> float:
        """Obtém o valor inicial dos limites do usuário (se existir)."""
        uc = self.usuario_controller
        if not uc or not getattr(uc, "usuario", None):
            return 0.0
        if tipo == "assinaturas":
            return float(uc.get_limite_assinaturas())
        return float(uc.get_limite_contratos())

    # ---------------- ACTIONS ----------------
    def _salvar_limite_ass(self):
        """Lê o valor digitado e atualiza o limite de assinaturas."""
        try:
            raw = self.entry_ass.get().strip().replace(",", ".")  # aceita vírgula
            valor = float(raw)
            uc = self.usuario_controller
            if uc and getattr(uc, "usuario", None):
                novo = uc.definir_limite_assinaturas(valor)  # salva no banco sem abreviar
                self.label_ass.config(text=self._format_display(novo))
            else:
                self.label_ass.config(text=self._format_display(valor))
            messagebox.showinfo("Sucesso", "Limite de assinaturas atualizado!")
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.")

    def _salvar_limite_con(self):
        """Lê o valor digitado e atualiza o limite de contratos."""
        try:
            raw = self.entry_con.get().strip().replace(",", ".")
            valor = float(raw)
            uc = self.usuario_controller
            if uc and getattr(uc, "usuario", None):
                novo = uc.definir_limite_contratos(valor)  # salva no banco sem abreviar
                self.label_con.config(text=self._format_display(novo))
            else:
                self.label_con.config(text=self._format_display(valor))
            messagebox.showinfo("Sucesso", "Limite de contratos atualizado!")
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.")
