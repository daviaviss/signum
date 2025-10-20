import tkinter as tk
from tkinter import messagebox, PhotoImage
from mvc import ui_constants as UI
from mvc.views.metas_view import MetasView
from mvc.views.perfil_view import PerfilView



class UserLoginView:
    """
    View do sistema de login/registro simplificada.
    - Caixas centralizadas para login e registro.
    - Um único estilo de botão.
    - Entrys com placeholders.
    """

    # ---------------- WINDOW ----------------
    WIDTH  = UI.WIDTH
    HEIGHT = UI.HEIGHT
    BG_COLOR = UI.BG_COLOR  # fundo da janela

    # ---------------- FRAME / BOX ----------------
    BOX_BG = UI.BOX_BG
    BOX_PAD_X = UI.BOX_PAD_X
    BOX_PAD_Y = UI.BOX_PAD_Y
    BOX_RELIEF = UI.BOX_RELIEF
    BOX_BORDER = UI.BOX_BORDER

    # ---------------- FONTS ----------------
    FONT_TITLE = UI.FONT_TITLE
    FONT_LABEL = UI.FONT_LABEL
    FONT_ENTRY = UI.FONT_ENTRY
    FONT_BUTTON = UI.FONT_BUTTON

    PAD_Y = UI.PAD_Y

    # ---------------- BUTTON COLORS ----------------
    BTN_BG = UI.BTN_BG
    BTN_FG = UI.BTN_FG
    BTN_ACTIVE_BG = UI.BTN_ACTIVE_BG
    BTN_ACTIVE_FG = UI.BTN_ACTIVE_FG

    # ---------------- ENTRY COLORS ----------------
    ENTRY_BG = UI.ENTRY_BG
    ENTRY_FG = UI.ENTRY_FG
    ENTRY_PLACEHOLDER_FG = UI.ENTRY_PLACEHOLDER_FG
    ENTRY_CURSOR_COLOR = UI.ENTRY_CURSOR_COLOR

    def __init__(self, root):
        self.root = root
        self.root.title("Signum")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_COLOR)

        # Frames
        self.register_frame = tk.Frame(root, bg=self.BG_COLOR)
        self.login_frame = tk.Frame(root, bg=self.BG_COLOR)
        self.home_frame = tk.Frame(root, bg=self.BG_COLOR)

        # Criar telas
        self._create_register_screen()
        self._create_login_screen()
        self._create_home_screen()

        self.show_register_screen()
        
        

    # ---------------- PLACEHOLDER HELPER ----------------
    def _add_placeholder(self, entry, text):
        def on_focus_in(event):
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(fg=self.ENTRY_FG)

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg=self.ENTRY_PLACEHOLDER_FG)

        entry.insert(0, text)
        entry.config(fg=self.ENTRY_PLACEHOLDER_FG)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # ---------------- REGISTER SCREEN ----------------
    def _create_register_screen(self):
        box = tk.Frame(
            self.register_frame, bg=self.BOX_BG,
            padx=self.BOX_PAD_X, pady=self.BOX_PAD_Y,
            relief=self.BOX_RELIEF, borderwidth=self.BOX_BORDER
        )
        box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(box, text="Registre-se", font=self.FONT_TITLE, bg=self.BOX_BG, fg="#2e3047").pack(pady=self.PAD_Y)

        self.reg_name = tk.Entry(box, font=self.FONT_ENTRY, width=30,
                                 bg=self.ENTRY_BG, fg=self.ENTRY_FG,
                                 insertbackground=self.ENTRY_CURSOR_COLOR)
        self.reg_name.pack(pady=self.PAD_Y)
        self._add_placeholder(self.reg_name, "Digite seu nome completo...")

        self.reg_email = tk.Entry(box, font=self.FONT_ENTRY, width=30,
                                  bg=self.ENTRY_BG, fg=self.ENTRY_FG,
                                  insertbackground=self.ENTRY_CURSOR_COLOR)
        self.reg_email.pack(pady=self.PAD_Y)
        self._add_placeholder(self.reg_email, "Digite seu email...")

        self.reg_password = tk.Entry(box, font=self.FONT_ENTRY, width=30,
                                     bg=self.ENTRY_BG, fg=self.ENTRY_FG,
                                     insertbackground=self.ENTRY_CURSOR_COLOR, show="*")
        self.reg_password.pack(pady=self.PAD_Y)
        self._add_placeholder(self.reg_password, "Digite sua senha...")

        self.register_button = tk.Button(
            box, text="Registrar",
            font=self.FONT_BUTTON,
            bg="#8cb0e5", fg=self.BTN_FG,
            activebackground=self.BTN_ACTIVE_BG,
            activeforeground=self.BTN_ACTIVE_FG,
            relief="flat", borderwidth=0, width=20,
            command=lambda: None  # será ligado ao Controller
        )
        self.register_button.pack(pady=self.PAD_Y)

        self.switch_to_login_button = tk.Button(
            box, text="Ir para Login",
            font=self.FONT_BUTTON,
            bg=self.BTN_BG, fg=self.BTN_FG,
            relief="flat", borderwidth=0, width=20,
            command=self.show_login_screen
        )
        self.switch_to_login_button.pack(pady=self.PAD_Y)

    # ---------------- LOGIN SCREEN ----------------
    def _create_login_screen(self):
        box = tk.Frame(
            self.login_frame, bg=self.BOX_BG,
            padx=self.BOX_PAD_X, pady=self.BOX_PAD_Y,
            relief=self.BOX_RELIEF, borderwidth=self.BOX_BORDER
        )
        box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(box, text="Login", font=self.FONT_TITLE, bg=self.BOX_BG, fg="#2e3047").pack(pady=self.PAD_Y)

        self.login_email = tk.Entry(box, font=self.FONT_ENTRY, width=30,
                                    bg=self.ENTRY_BG, fg=self.ENTRY_FG,
                                    insertbackground=self.ENTRY_CURSOR_COLOR)
        self.login_email.pack(pady=self.PAD_Y)
        self._add_placeholder(self.login_email, "Digite seu email...")

        self.login_password = tk.Entry(box, font=self.FONT_ENTRY, width=30,
                                       bg=self.ENTRY_BG, fg=self.ENTRY_FG,
                                       insertbackground=self.ENTRY_CURSOR_COLOR, show="*")
        self.login_password.pack(pady=self.PAD_Y)
        self._add_placeholder(self.login_password, "Digite sua senha...")

        self.login_button = tk.Button(
            box, text="Login",
            font=self.FONT_BUTTON,
            bg=self.BTN_BG, fg=self.BTN_FG,
            activebackground=self.BTN_ACTIVE_BG,
            activeforeground=self.BTN_ACTIVE_FG,
            relief="flat", borderwidth=0, width=20,
            command=lambda: None  # será ligado ao Controller
        )
        self.login_button.pack(pady=self.PAD_Y)

        self.switch_to_register_button = tk.Button(
            box, text="Registrar-se",
            font=self.FONT_BUTTON,
            bg=self.BTN_BG, fg=self.BTN_FG,
            activebackground=self.BTN_ACTIVE_BG,
            activeforeground=self.BTN_ACTIVE_FG,
            relief="flat", borderwidth=0, width=20,
            command=self.show_register_screen
        )
        self.switch_to_register_button.pack(pady=self.PAD_Y)
    
    # ---------------- NAVBAR COMUM ----------------
    def _render_navbar(self, parent, active: str):
        """Desenha o navbar no frame 'parent' e pinta de azul o item ativo (Assinaturas, Contratos, Metas)."""
        header_height = 60
        header = tk.Frame(parent, bg=self.BOX_BG, height=header_height)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Ícones
        self.home_img = tk.PhotoImage(file="static/home.png")
        self.profile_img = tk.PhotoImage(file="static/profile.png")

        # Ícone de Home (esquerda)
        home_btn = tk.Label(header, image=self.home_img, bg=self.BOX_BG, cursor="hand2")
        home_btn.pack(side="left", padx=10)
        home_btn.bind("<Button-1>", lambda e: self.show_home_screen())

        # Links centrais
        center = tk.Frame(header, bg=self.BOX_BG)
        center.pack(side="left", expand=True)

        def link(text, cmd):
            fg = "#1a56db" if text.lower() == active.lower() else self.BTN_FG
            lbl = tk.Label(center, text=text, font=self.FONT_BUTTON, bg=self.BOX_BG, fg=fg, cursor="hand2")
            lbl.pack(side="left", padx=15)
            lbl.bind("<Button-1>", lambda e: cmd())
            return lbl

        link("Assinaturas", lambda: self.show_message("Assinaturas", "Você clicou em Assinaturas"))
        link("Contratos", lambda: self.show_message("Contratos", "Você clicou em Contratos"))
        link("Metas", self.show_metas_screen)

        # Ícone de perfil (direita)
        profile_btn = tk.Label(header, image=self.profile_img, bg=self.BOX_BG, cursor="hand2")
        profile_btn.pack(side="right", padx=10)
        profile_btn.bind("<Button-1>", lambda e: self.show_profile_screen())


    # ---------------- HOME SCREEN ----------------
    def _create_home_screen(self):
        for widget in self.home_frame.winfo_children():
            widget.destroy()

        self.home_frame.pack(fill="both", expand=True)

        # ---------------- HEADER ----------------
        self._render_navbar(self.home_frame, active="")

        # ---------------- CONTEÚDO ----------------
        content_frame = tk.Frame(self.home_frame, bg=self.BG_COLOR)
        content_frame.pack(fill="both", expand=True)

        # Dividir a tela em 2: esquerda 1/3, direita 2/3
        left_frame = tk.Frame(content_frame, bg=self.BG_COLOR, width=int(self.WIDTH / 3))
        left_frame.pack(side="left", fill="y", padx=20, pady=20)
        left_frame.pack_propagate(False)  # respeitar altura do frame

        right_frame = tk.Frame(content_frame, bg=self.BG_COLOR)
        right_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Botões verticais ocupando todo o espaço do left_frame
        btn_names = ["Assinaturas", "Contratos", "Metas"]
        for name in btn_names:
            cmd = self.show_metas_screen if name == "Metas" else \
                  (lambda n=name: self.show_message(n, f"Você clicou em {n}"))

            btn = tk.Button(
                left_frame, text=name, font=("Inter", 18, "bold"),
                bg=self.BTN_BG, fg=self.BTN_FG,
                activebackground=self.BTN_ACTIVE_BG,
                activeforeground=self.BTN_ACTIVE_FG,
                relief="flat", borderwidth=0,
                command=cmd
            )
            btn.pack(fill="both", expand=True, pady=25, padx=5)  # fill vertical e expand para ocupar espaço
        # ----- PRÉVIA DAS METAS NA HOME (sem inputs/botões) -----
        # pega os valores atuais do controller, se houver usuário vinculado
        uc = getattr(self, "usuario_controller", None)
        if uc and getattr(uc, "usuario", None):
            val_ass = float(uc.get_limite_assinaturas())
            val_con = float(uc.get_limite_contratos())
        else:
            val_ass = 0.0
            val_con = 0.0

        # container que expande e mantém o row centralizado
        cards_container = tk.Frame(right_frame, bg=self.BG_COLOR)
        cards_container.pack(fill="both", expand=True)
        
        
        # Centraliza HORIZONTAL e faz espaçadores VERTICAIS iguais
        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=0)
        cards_container.grid_columnconfigure(2, weight=1)

        cards_container.grid_rowconfigure(0, weight=1)  # espaçador superior
        cards_container.grid_rowconfigure(2, weight=1)  # espaçador inferior

        mini_row = tk.Frame(cards_container, bg=self.BG_COLOR)
        mini_row.grid(row=1, column=1)  # linha do meio → espaços iguais em cima/baixo


        self._home_meta_card(mini_row, "Assinaturas", val_ass)
        self._home_meta_card(mini_row, "Contratos",   val_con)

    # --------- FORMATADOR PARA MOSTRAR metas NA HOME (abreviado) ---------
    def _format_metas_display(self, valor: float) -> str:
        sign = "-" if valor < 0 else ""
        v = abs(float(valor))
        if v >= 1_000_000:
            n = v / 1_000_000
            num = f"{n:.1f}" if n % 1 else f"{int(n)}"
            num = num.replace(".", ",")
            return f"{sign}R${num}M"
        if v >= 10_000:
            n = v / 1_000
            num = f"{n:.1f}" if n % 1 else f"{int(n)}"
            num = num.replace(".", ",")
            return f"{sign}R${num}mil"
        # BRL normal para menores de 10k
        s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{sign}R${s}"

    def _home_meta_card(self, parent, titulo: str, valor: float):
        box_bg = getattr(UI, "BOX_CARD_BG", "#d9d9d9")

        # tamanho do card
        CARD_W, CARD_H = 350, 290
        card = tk.Frame(parent, bg=box_bg, bd=2, relief="groove",
                        width=CARD_W, height=CARD_H)
        card.pack(side="top", pady=6)
        card.pack_propagate(False)

        tk.Label(card, text=titulo, font=("Arial", 12, "bold"), bg=box_bg)\
        .pack(pady=(6, 6))

        # área central com grid para espaço igual em cima/baixo
        center = tk.Frame(card, bg=box_bg)
        center.pack(fill="both", expand=True)

        center.grid_rowconfigure(0, weight=1)
        center.grid_rowconfigure(2, weight=1)
        center.grid_columnconfigure(0, weight=1)

        # círculo
        circle = tk.PhotoImage(file="static/circle.png").zoom(2, 2).subsample(5, 5)
        if not hasattr(self, "_home_imgs"):
            self._home_imgs = []
        self._home_imgs.append(circle)  # evita GC

        circle_lbl = tk.Label(center, image=circle, bg=box_bg, bd=0, highlightthickness=0)
        circle_lbl.grid(row=1, column=0)

        # valor centralizado no círculo
        val_lbl = tk.Label(center,
                        text=self._format_metas_display(valor),
                        font=("Arial", 12, "bold"),
                        bg=box_bg)
        val_lbl.place(in_=circle_lbl, relx=0.5, rely=0.5, anchor="center")





    # ---------------- METAS SCREEN ----------------
    def show_metas_screen(self):
        """Mostra a tela Metas: navbar comum (Metas ativo) + conteúdo MetasView."""
        # Limpa e exibe o frame principal
        for w in self.home_frame.winfo_children():
            w.destroy()
        self.home_frame.pack(fill="both", expand=True)

        # Navbar com 'Metas' ativo
        self._render_navbar(self.home_frame, active="Metas")

        # Área de conteúdo
        content = tk.Frame(self.home_frame, bg=self.BG_COLOR)
        content.pack(fill="both", expand=True)

        # Instancia o conteúdo da tela Metas (arquivo separado)
        # Se o controller de usuário tiver sido setado no main, ele será usado aqui
        self.metas_view = MetasView(content, getattr(self, "usuario_controller", None))
    
    # ---------------- SCREEN SWITCHING ----------------
    def show_register_screen(self):
        self._hide_all_frames()
        self.register_frame.pack(fill="both", expand=True)

    def show_login_screen(self):
        self._hide_all_frames()
        self.login_frame.pack(fill="both", expand=True)

    def show_home_screen(self):
        self._hide_all_frames()
        self.home_frame.pack(fill="both", expand=True)
        self._create_home_screen()

    def show_profile_screen(self):
        """Mostra a tela de perfil do usuário."""
        # Limpa e exibe o frame principal
        for w in self.home_frame.winfo_children():
            w.destroy()
        self.home_frame.pack(fill="both", expand=True)

        # Navbar com nenhum item ativo
        self._render_navbar(self.home_frame, active="")

        # Área de conteúdo
        content = tk.Frame(self.home_frame, bg=self.BG_COLOR)
        content.pack(fill="both", expand=True)

        # Instancia a view de perfil
        self.perfil_view = PerfilView(content, self.usuario_controller)

    def _hide_all_frames(self):
        self.register_frame.pack_forget()
        self.login_frame.pack_forget()
        self.home_frame.pack_forget()

    # ---------------- MESSAGES ----------------
    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)