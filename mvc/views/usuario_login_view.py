import tkinter as tk
from tkinter import messagebox, PhotoImage


class UserLoginView:
    """
    View do sistema de login/registro simplificada.
    - Caixas centralizadas para login e registro.
    - Um único estilo de botão.
    - Entrys com placeholders.
    """

    # ---------------- WINDOW ----------------
    WIDTH = 1024
    HEIGHT = 720
    BG_COLOR = "#f9faf2"  # fundo da janela

    # ---------------- FRAME / BOX ----------------
    BOX_BG = "#edede6"  # fundo das caixas
    BOX_PAD_X = 40
    BOX_PAD_Y = 30
    BOX_RELIEF = "raised"
    BOX_BORDER = 2

    # ---------------- FONTS ----------------
    FONT_TITLE = ("Inter", 24, "bold")
    FONT_LABEL = ("Inter", 14)
    FONT_ENTRY = ("Inter", 12)
    FONT_BUTTON = ("Inter", 12, "bold")

    PAD_Y = 10

    # ---------------- BUTTON COLORS ----------------
    BTN_BG = "#8cb0e5"
    BTN_FG = "#2e3047"
    BTN_ACTIVE_BG = "#c1d7ff"
    BTN_ACTIVE_FG = "#2e3047"

    # ---------------- ENTRY COLORS ----------------
    ENTRY_BG = "#a5b3b6"
    ENTRY_FG = "#2e3047"
    ENTRY_PLACEHOLDER_FG = "#ffffff"
    ENTRY_CURSOR_COLOR = "#2e3047"

    def __init__(self, root):
        self.root = root
        self.root.title("User System (MVC)")
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

    # ---------------- HOME SCREEN ----------------
    def _create_home_screen(self):
        for widget in self.home_frame.winfo_children():
            widget.destroy()

        self.home_frame.pack(fill="both", expand=True)

        # ---------------- HEADER ----------------
        header_height = 60
        header = tk.Frame(self.home_frame, bg=self.BTN_BG, height=header_height)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Carregar imagens
        self.home_img = tk.PhotoImage(file="static/home.png")
        self.profile_img = tk.PhotoImage(file="static/profile.png")

        # Home image à esquerda
        home_btn = tk.Label(header, image=self.home_img, bg=self.BTN_BG, cursor="hand2")
        home_btn.pack(side="left", padx=10)
        home_btn.bind("<Button-1>", lambda e: self.show_message("Home", "Você clicou no Home"))

        # Links centrais (text labels clicáveis)
        center_frame = tk.Frame(header, bg=self.BTN_BG)
        center_frame.pack(side="left", expand=True)

        def create_link(parent, text, command):
            lbl = tk.Label(parent, text=text, font=self.FONT_BUTTON, bg=self.BTN_BG, fg=self.BTN_FG, cursor="hand2")
            lbl.pack(side="left", padx=15)
            lbl.bind("<Button-1>", lambda e: command())
            return lbl

        assinaturas_lbl = create_link(center_frame, "Assinaturas", lambda: self.show_message("Assinaturas", "Você clicou em Assinaturas"))
        contratos_lbl = create_link(center_frame, "Contratos", lambda: self.show_message("Contratos", "Você clicou em Contratos"))
        metas_lbl = create_link(center_frame, "Metas", lambda: self.show_message("Metas", "Você clicou em Metas"))

        # Perfil image à direita
        profile_btn = tk.Label(header, image=self.profile_img, bg=self.BTN_BG, cursor="hand2")
        profile_btn.pack(side="right", padx=10)
        profile_btn.bind("<Button-1>", lambda e: self.show_message("Perfil", "Você clicou no Perfil"))

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
            btn = tk.Button(
                left_frame, text=name, font=("Inter", 18, "bold"),
                bg=self.BTN_BG, fg=self.BTN_FG,
                activebackground=self.BTN_ACTIVE_BG,
                activeforeground=self.BTN_ACTIVE_FG,
                relief="flat", borderwidth=0,
                command=lambda n=name: self.show_message(n, f"Você clicou em {n}")
            )
            btn.pack(fill="both", expand=True, pady=25, padx=5)  # fill vertical e expand para ocupar espaço

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

    def _hide_all_frames(self):
        self.register_frame.pack_forget()
        self.login_frame.pack_forget()
        self.home_frame.pack_forget()

    # ---------------- MESSAGES ----------------
    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)