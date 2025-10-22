import tkinter as tk
from mvc import ui_constants as UI


class ContratosView:
    """View para tela de Contratos."""
    
    def __init__(self, parent, controller=None):
        self.parent = parent
        self.controller = controller
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
        
        # Container para o conteúdo
        content = tk.Frame(self.parent, bg=UI.BG_COLOR)
        content.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Área de lista (será populada pelo controller)
        self.lista_frame = tk.Frame(content, bg=UI.BOX_BG, relief="groove", bd=2)
        self.lista_frame.pack(fill="both", expand=True)
        
        # Label quando vazio
        self.empty_label = tk.Label(
            self.lista_frame,
            text="Nenhum contrato cadastrado",
            font=UI.FONT_LABEL,
            bg=UI.BOX_BG,
            fg="#666"
        )
        self.empty_label.pack(pady=50)
    
    def atualizar_lista(self, contratos):
        """Atualiza a lista de contratos exibida."""
        # Limpa o frame
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        
        if not contratos:
            self.empty_label = tk.Label(
                self.lista_frame,
                text="Nenhum contrato cadastrado",
                font=UI.FONT_LABEL,
                bg=UI.BOX_BG,
                fg="#666"
            )
            self.empty_label.pack(pady=50)
        else:
            for contrato in contratos:
                item = tk.Frame(self.lista_frame, bg=UI.BOX_CARD_BG, relief="raised", bd=1)
                item.pack(fill="x", padx=10, pady=5)
                
                tk.Label(
                    item,
                    text=f"{contrato.nome} - R$ {contrato.valor:.2f} - {contrato.data}",
                    font=UI.FONT_LABEL,
                    bg=UI.BOX_CARD_BG,
                    anchor="w"
                ).pack(side="left", padx=10, pady=10, fill="x", expand=True)
