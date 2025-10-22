import tkinter as tk
from mvc import ui_constants as UI


class LoginView:
    """View for user login screen."""

    def __init__(self, parent, switch_to_register_callback):
        self.parent = parent
        self.switch_to_register_callback = switch_to_register_callback
        self.frame = tk.Frame(parent, bg=UI.BG_COLOR)
        self._placeholders = {}
        self._create_ui()

    def _add_placeholder(self, entry, text):
        def on_focus_in(event):
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(fg=UI.ENTRY_FG)

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg=UI.ENTRY_PLACEHOLDER_FG)

        entry.insert(0, text)
        entry.config(fg=UI.ENTRY_PLACEHOLDER_FG)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        # Store placeholder text for validation
        self._placeholders[entry] = text

    def get_field_value(self, entry):
        """Get field value, returning empty string if it's still a placeholder."""
        value = entry.get().strip()
        if entry in self._placeholders and value == self._placeholders[entry]:
            return ""
        return value

    def validate_fields(self):
        """Validate that all fields are filled with real data."""
        email = self.get_field_value(self.login_email)
        senha = self.get_field_value(self.login_password)

        if not email:
            return False, "Por favor, preencha seu email."
        if not senha:
            return False, "Por favor, preencha sua senha."
        if "@" not in email:
            return False, "Por favor, insira um email válido."

        return True, ""

    def _create_ui(self):
        box = tk.Frame(
            self.frame, bg=UI.BOX_BG,
            padx=UI.BOX_PAD_X, pady=UI.BOX_PAD_Y,
            relief=UI.BOX_RELIEF, borderwidth=UI.BOX_BORDER
        )
        box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(box, text="Login", font=UI.FONT_TITLE, bg=UI.BOX_BG, fg="#2e3047").pack(pady=UI.PAD_Y)

        self.login_email = tk.Entry(box, font=UI.FONT_ENTRY, width=30,
                                    bg=UI.ENTRY_BG, fg=UI.ENTRY_FG,
                                    insertbackground=UI.ENTRY_CURSOR_COLOR)
        self.login_email.pack(pady=UI.PAD_Y)
        self._add_placeholder(self.login_email, "Digite seu email...")

        self.login_password = tk.Entry(box, font=UI.FONT_ENTRY, width=30,
                                       bg=UI.ENTRY_BG, fg=UI.ENTRY_FG,
                                       insertbackground=UI.ENTRY_CURSOR_COLOR, show="*")
        self.login_password.pack(pady=UI.PAD_Y)
        self._add_placeholder(self.login_password, "Digite sua senha...")

        self.login_button = tk.Button(
            box, text="Login",
            font=UI.FONT_BUTTON,
            bg=UI.BTN_BG, fg=UI.BTN_FG,
            activebackground=UI.BTN_ACTIVE_BG,
            activeforeground=UI.BTN_ACTIVE_FG,
            relief="flat", borderwidth=0, width=20,
            command=lambda: None
        )
        self.login_button.pack(pady=UI.PAD_Y)

        self.switch_to_register_button = tk.Button(
            box, text="Registrar-se",
            font=UI.FONT_BUTTON,
            bg=UI.BTN_BG, fg=UI.BTN_FG,
            activebackground=UI.BTN_ACTIVE_BG,
            activeforeground=UI.BTN_ACTIVE_FG,
            relief="flat", borderwidth=0, width=20,
            command=self.switch_to_register_callback
        )
        self.switch_to_register_button.pack(pady=UI.PAD_Y)

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
