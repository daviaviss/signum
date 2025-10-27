import tkinter as tk
from tkinter import messagebox
from mvc import ui_constants as UI

class PerfilView:
    def __init__(self, parent, usuario_controller, on_profile_updated=None):
        self.parent = parent
        self.usuario_controller = usuario_controller
        self.usuario = usuario_controller.usuario
        self.on_profile_updated = on_profile_updated
        self._placeholders = {}
        self._create_profile_screen()

    def _add_placeholder(self, entry, text, is_password=False):
        def on_focus_in(event):
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(fg=UI.ENTRY_FG)
                if is_password:
                    entry.config(show="*")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg=UI.ENTRY_PLACEHOLDER_FG)
                if is_password:
                    entry.config(show="")

        # Only insert placeholder initially if field is empty
        if not entry.get():
            entry.insert(0, text)
            entry.config(fg=UI.ENTRY_PLACEHOLDER_FG)
            if is_password:
                entry.config(show="")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        self._placeholders[entry] = text

    def get_field_value(self, entry):
        value = entry.get().strip()
        if entry in self._placeholders and value == self._placeholders[entry]:
            return ""
        return value

    def _create_profile_screen(self):
        box = tk.Frame(
            self.parent, bg=UI.BOX_BG,
            padx=UI.BOX_PAD_X, pady=UI.BOX_PAD_Y,
            relief=UI.BOX_RELIEF, borderwidth=UI.BOX_BORDER
        )
        box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(box, text="Editar Perfil", font=UI.FONT_TITLE, bg=UI.BOX_BG, fg="#2e3047").pack(pady=UI.PAD_Y)

        # Nome
        self.name_entry = tk.Entry(box, font=UI.FONT_ENTRY, width=30,
                                 bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.name_entry.insert(0, self.usuario.nome)
        self.name_entry.pack(pady=UI.PAD_Y)
        # Add placeholder when field is cleared
        self._add_placeholder(self.name_entry, "Seu nome completo...")

        # Email (não editável)
        self.email_entry = tk.Entry(box, font=UI.FONT_ENTRY, width=30,
                                  bg=UI.ENTRY_BG, fg=UI.ENTRY_FG)
        self.email_entry.insert(0, self.usuario.email)
        self.email_entry.config(state="disabled")
        self.email_entry.pack(pady=UI.PAD_Y)

        # Senha
        self.password_entry = tk.Entry(box, font=UI.FONT_ENTRY, width=30,
                                    bg=UI.ENTRY_BG, fg=UI.ENTRY_FG, show="*")
        self.password_entry.pack(pady=UI.PAD_Y)
        # Placeholder visível para senha quando vazia
        self._add_placeholder(self.password_entry, "Nova senha...", is_password=True)
        tk.Label(box, text="Deixe em branco para manter a senha atual", 
                font=("Inter", 8), bg=UI.BOX_BG).pack()

        # Botão Salvar
        self.save_button = tk.Button(
            box, text="Salvar Alterações",
            font=UI.FONT_BUTTON,
            bg=UI.BTN_BG, fg=UI.BTN_FG,
            activebackground=UI.BTN_ACTIVE_BG,
            activeforeground=UI.BTN_ACTIVE_FG,
            relief="flat", borderwidth=0, width=20,
            command=self.save_profile
        )
        self.save_button.pack(pady=UI.PAD_Y)

    def save_profile(self):
        new_name = self.get_field_value(self.name_entry)
        new_email = self.usuario.email  # e-mail permanece o atual, não editável
        new_password = self.get_field_value(self.password_entry)

        # Validações alinhadas ao cadastro
        if not new_name:
            messagebox.showerror("Erro de Validação", "Por favor, preencha seu nome completo.")
            return
        if new_password and len(new_password) < 6:
            messagebox.showerror("Erro de Validação", "A senha deve ter pelo menos 6 caracteres.")
            return

        try:
            self.usuario_controller.update_profile(new_name, new_email, new_password)
            # Atualiza visual da sidebar se callback disponível
            if callable(self.on_profile_updated):
                self.on_profile_updated()
            messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
