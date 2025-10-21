import tkinter as tk
from mvc import ui_constants as UI

class NavbarView:
    """
    Componente de navbar reutilizável para o sistema.
    Pode ser incluído em qualquer tela que precise de navegação.
    """

    def __init__(self, parent, active="", callback_dict=None):
        """
        Inicializa a navbar.
        
        Args:
            parent: Frame pai onde a navbar será renderizada
            active: String com o nome do item ativo (será destacado)
            callback_dict: Dicionário com callbacks para cada item do menu
        """
        self.parent = parent
        self.active = active
        self.callback_dict = callback_dict or {}
        
        # Constantes de UI
        self.BOX_BG = UI.BOX_BG
        self.BTN_FG = UI.BTN_FG
        self.BTN_BG = UI.BTN_BG
        self.FONT_BUTTON = UI.FONT_BUTTON
        
        # Imagens
        self.home_img = None
        self.profile_img = None
        
        # Renderiza a navbar
        self._render_navbar()
    
    def _render_navbar(self):
        """Desenha o navbar no frame 'parent' e pinta de azul o item ativo."""
        header_height = 60
        self.header = tk.Frame(self.parent, bg=self.BOX_BG, height=header_height)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        # Carrega ícones
        self.home_img = tk.PhotoImage(file="static/home.png")
        self.profile_img = tk.PhotoImage(file="static/profile.png")

        # Ícone de Home (esquerda)
        home_btn = tk.Label(self.header, image=self.home_img, bg=self.BOX_BG, cursor="hand2")
        home_btn.pack(side="left", padx=10)
        home_btn.bind("<Button-1>", lambda e: self._call_callback("home"))

        # Links centrais
        center = tk.Frame(self.header, bg=self.BOX_BG)
        center.pack(side="left", expand=True)

        # Cria os links de navegação
        self._create_link(center, "Assinaturas", "assinaturas")
        self._create_link(center, "Contratos", "contratos")
        self._create_link(center, "Metas", "metas")

        # Ícone de perfil (direita)
        profile_btn = tk.Label(self.header, image=self.profile_img, bg=self.BOX_BG, cursor="hand2")
        profile_btn.pack(side="right", padx=10)
        profile_btn.bind("<Button-1>", lambda e: self._call_callback("profile"))
    
    def _create_link(self, parent, text, callback_key):
        """Cria um link de navegação na navbar."""
        fg = "#1a56db" if text.lower() == self.active.lower() else self.BTN_FG
        lbl = tk.Label(parent, text=text, font=self.FONT_BUTTON, bg=self.BOX_BG, fg=fg, cursor="hand2")
        lbl.pack(side="left", padx=15)
        lbl.bind("<Button-1>", lambda e: self._call_callback(callback_key))
        return lbl
    
    def _call_callback(self, key):
        """Chama o callback associado à chave, se existir."""
        if key in self.callback_dict and callable(self.callback_dict[key]):
            self.callback_dict[key]()