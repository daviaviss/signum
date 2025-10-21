# dao.py
import sqlite3
from typing import Optional
from mvc.models.usuario_model import Usuario

class UserDAO:
    def __init__(self, db_file="database.sqlite"):
        self.conn = sqlite3.connect(db_file)
        self._create_table()
        self._ensure_limit_columns()  # garante colunas mesmo se DB já existir

    # ---------------- SCHEMA ----------------
    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            limite_assinaturas REAL NOT NULL DEFAULT 0,
            limite_contratos REAL NOT NULL DEFAULT 0
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def _ensure_limit_columns(self):
        # Se o banco for antigo (sem colunas), adiciona via ALTER TABLE
        cur = self.conn.execute("PRAGMA table_info(users)")
        cols = {row[1] for row in cur.fetchall()}
        altered = False
        if "limite_assinaturas" not in cols:
            self.conn.execute(
                "ALTER TABLE users ADD COLUMN limite_assinaturas REAL NOT NULL DEFAULT 0"
            )
            altered = True
        if "limite_contratos" not in cols:
            self.conn.execute(
                "ALTER TABLE users ADD COLUMN limite_contratos REAL NOT NULL DEFAULT 0"
            )
            altered = True
        if altered:
            self.conn.commit()

    # ---------------- CREATE ----------------
    def add_user(self, user: Usuario):
        query = """
            INSERT INTO users (nome, email, senha_hash, limite_assinaturas, limite_contratos)
            VALUES (?, ?, ?, ?, ?)
        """
        self.conn.execute(
            query,
            (
                user.nome,
                user.email,
                user.senha_hash,
                float(user.limite_assinaturas),
                float(user.limite_contratos),
            ),
        )
        self.conn.commit()

    # ---------------- READ ----------------
    def get_user_by_email(self, email: str) -> Optional[Usuario]:
        cursor = self.conn.execute(
            """
            SELECT id, nome, email, senha_hash, limite_assinaturas, limite_contratos
            FROM users WHERE email=?
            """,
            (email,),
        )
        row = cursor.fetchone()
        if row:
            user_id, nome, email_db, senha_hash, lim_ass, lim_con = row
            # cria o Usuario sem re-hash de senha (vamos injetar o hash persistido)
            user = Usuario(
                nome=nome,
                email=email_db,
                senha="",
                user_id=user_id,
                limite_assinaturas=lim_ass,
                limite_contratos=lim_con,
            )
            user.senha_hash = senha_hash
            return user
        return None

    # ---------------- UPDATE (apenas limites) ----------------
    def update_user_limits(
        self,
        user_id: int,
        limite_assinaturas: float,
        limite_contratos: float,
    ) -> None:
        self.conn.execute(
            """
            UPDATE users
               SET limite_assinaturas = ?, limite_contratos = ?
             WHERE id = ?
            """,
            (float(limite_assinaturas), float(limite_contratos), user_id),
        )
        self.conn.commit()

    # ---------------- UPDATE PROFILE ----------------
    def update_user_profile(self, user_id: int, nome: str, email: str, senha_hash: str) -> None:
        self.conn.execute(
            """
            UPDATE users
               SET nome = ?, email = ?, senha_hash = ?
             WHERE id = ?
            """,
            (nome, email, senha_hash, user_id)
        )
        self.conn.commit()
