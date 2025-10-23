import tkinter as tk
from tkinter import messagebox
from mvc import ui_constants as UI
from mvc.views.metas_view import MetasView
from mvc.views.perfil_view import PerfilView
from mvc.views.navbar_view import NavbarView
from mvc.views.assinaturas_view import AssinaturasView
from mvc.controllers.assinaturas_controller import AssinaturasController


class HomeView:
    """View for home screen with navigation."""

    def __init__(self, parent, usuario_controller=None):
        self.parent = parent
        self.usuario_controller = usuario_controller
        self.frame = tk.Frame(parent, bg=UI.BG_COLOR)
        self._home_imgs = []
        self.navbar = None
        self.metas_view = None
        self.perfil_view = None
        self.assinaturas_controller = None
        self.contratos_controller = None
        # Don't create home screen yet - will be created on first show

    def _render_navbar(self, parent, active: str):
        """Desenha o navbar no frame 'parent' e pinta de azul o item ativo."""
        callbacks = {
            "home": self.show_home_screen,
            "assinaturas": self.show_assinaturas_screen,
            "contratos": self.show_contratos_screen,
            "metas": self.show_metas_screen,
            "profile": self.show_profile_screen
        }
        
        self.navbar = NavbarView(parent, active=active, callback_dict=callbacks)

    def _create_home_screen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Header
        self._render_navbar(self.frame, active="")

        # Conteúdo
        content_frame = tk.Frame(self.frame, bg=UI.BG_COLOR)
        content_frame.pack(fill="both", expand=True)

        # Dividir em 2: esquerda 1/3, direita 2/3
        left_frame = tk.Frame(content_frame, bg=UI.BG_COLOR, width=int(UI.WIDTH / 3))
        left_frame.pack(side="left", fill="y", padx=20, pady=20)
        left_frame.pack_propagate(False)

        right_frame = tk.Frame(content_frame, bg=UI.BG_COLOR)
        right_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Botões verticais
        btn_names = ["Assinaturas", "Contratos", "Metas"]
        for name in btn_names:
            if name == "Metas":
                cmd = self.show_metas_screen
            elif name == "Assinaturas":
                cmd = self.show_assinaturas_screen
            elif name == "Contratos":
                cmd = self.show_contratos_screen
            else:
                cmd = lambda n=name: self.show_message(n, f"Você clicou em {n}")

            btn = tk.Button(
                left_frame, text=name, font=("Inter", 18, "bold"),
                bg=UI.BTN_BG, fg=UI.BTN_FG,
                activebackground=UI.BTN_ACTIVE_BG,
                activeforeground=UI.BTN_ACTIVE_FG,
                relief="flat", borderwidth=0,
                command=cmd
            )
            btn.pack(fill="both", expand=True, pady=25, padx=5)

        # Prévia das metas
        uc = self.usuario_controller
        if uc and getattr(uc, "usuario", None):
            val_ass = float(uc.get_limite_assinaturas())
            val_con = float(uc.get_limite_contratos())
        else:
            val_ass = 0.0
            val_con = 0.0

        cards_container = tk.Frame(right_frame, bg=UI.BG_COLOR)
        cards_container.pack(fill="both", expand=True)
        
        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=0)
        cards_container.grid_columnconfigure(2, weight=1)
        cards_container.grid_rowconfigure(0, weight=1)
        cards_container.grid_rowconfigure(2, weight=1)

        mini_row = tk.Frame(cards_container, bg=UI.BG_COLOR)
        mini_row.grid(row=1, column=1)

        self._home_meta_card(mini_row, "Assinaturas", val_ass)
        self._home_meta_card(mini_row, "Contratos", val_con)

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
        s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{sign}R${s}"

    def _home_meta_card(self, parent, titulo: str, valor: float):
        box_bg = getattr(UI, "BOX_CARD_BG", "#d9d9d9")
        CARD_W, CARD_H = 350, 290
        card = tk.Frame(parent, bg=box_bg, bd=2, relief="groove",
                        width=CARD_W, height=CARD_H)
        card.pack(side="top", pady=6)
        card.pack_propagate(False)

        tk.Label(card, text=titulo, font=("Arial", 12, "bold"), bg=box_bg)\
        .pack(pady=(6, 6))

        center = tk.Frame(card, bg=box_bg)
        center.pack(fill="both", expand=True)

        center.grid_rowconfigure(0, weight=1)
        center.grid_rowconfigure(2, weight=1)
        center.grid_columnconfigure(0, weight=1)

        circle = tk.PhotoImage(file="static/circle.png").zoom(2, 2).subsample(5, 5)
        self._home_imgs.append(circle)

        circle_lbl = tk.Label(center, image=circle, bg=box_bg, bd=0, highlightthickness=0)
        circle_lbl.grid(row=1, column=0)

        val_lbl = tk.Label(center,
                        text=self._format_metas_display(valor),
                        font=("Arial", 12, "bold"),
                        bg=box_bg)
        val_lbl.place(in_=circle_lbl, relx=0.5, rely=0.5, anchor="center")

    def show_metas_screen(self):
        """Mostra a tela Metas."""
        for w in self.frame.winfo_children():
            w.destroy()

        self._render_navbar(self.frame, active="Metas")

        content = tk.Frame(self.frame, bg=UI.BG_COLOR)
        content.pack(fill="both", expand=True)

        self.metas_view = MetasView(content, self.usuario_controller)

    def show_profile_screen(self):
        """Mostra a tela de perfil."""
        for w in self.frame.winfo_children():
            w.destroy()

        self._render_navbar(self.frame, active="")

        content = tk.Frame(self.frame, bg=UI.BG_COLOR)
        content.pack(fill="both", expand=True)

        self.perfil_view = PerfilView(content, self.usuario_controller)

    def show_assinaturas_screen(self):
        """Mostra a tela de Assinaturas."""
        for w in self.frame.winfo_children():
            w.destroy()

        self._render_navbar(self.frame, active="Assinaturas")

        content = tk.Frame(self.frame, bg=UI.BG_COLOR)
        content.pack(fill="both", expand=True)

        assinaturas_view = AssinaturasView(content)
        user_id = self.usuario_controller.usuario.id if self.usuario_controller and hasattr(self.usuario_controller, 'usuario') else None
        self.assinaturas_controller = AssinaturasController(assinaturas_view, user_id)

    def show_contratos_screen(self):
        """Mostra a tela de Contratos."""
        for w in self.frame.winfo_children():
            w.destroy()

        self._render_navbar(self.frame, active="Contratos")

        content = tk.Frame(self.frame, bg=UI.BG_COLOR)
        content.pack(fill="both", expand=True)

        contratos_view = ContratosView(content)
        self.contratos_controller = ContratosController(contratos_view)

    def show_home_screen(self):
        """Recarrega a home screen."""
        self._create_home_screen()

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show(self):
        self.frame.pack(fill="both", expand=True)
        # Create home screen content if not already created
        if not self.navbar:
            self._create_home_screen()

    def hide(self):
        self.frame.pack_forget()
