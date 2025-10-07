import sqlite3
from mvc.models.usuario_model import Usuario

class UserDAO:
    def __init__(self, db_file="database.sqlite"):
        self.conn = sqlite3.connect(db_file)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_user(self, user: Usuario):
        query = "INSERT INTO users (nome, email, senha_hash) VALUES (?, ?, ?)"
        self.conn.execute(query, (user.nome, user.email, user.senha_hash))
        self.conn.commit()

    def get_user_by_email(self, email: str) -> Usuario | None:
        cursor = self.conn.execute("SELECT id, nome, email, senha_hash FROM users WHERE email=?", (email,))
        row = cursor.fetchone()
        if row:
            user_id, nome, email, senha_hash = row
            user = Usuario(nome=nome, email=email, senha="")  # senha vazio só para criar objeto
            user.id = user_id
            user.senha_hash = senha_hash
            return user
        return None