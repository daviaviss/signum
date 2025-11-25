# dao.py
import sqlite3
from typing import Optional, List
from datetime import datetime
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
    
    # ---------------- GET USER ID BY EMAIL ----------------
    def get_user_id_by_email(self, email: str) -> Optional[int]:
        """
        Retorna o ID do usuário baseado no email.
        
        Args:
            email: Email do usuário
            
        Returns:
            ID do usuário ou None se não encontrado
        """
        cursor = self.conn.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()
        return row[0] if row else None

class PagamentosDAO:
    """DAO para gerenciar pagamentos no banco de dados."""
    
    def __init__(self, db_file="database.sqlite", user_id=None):
        self.conn = sqlite3.connect(db_file)
        self.user_id = user_id
        self._drop_and_create_table()
    
    def set_user_id(self, user_id):
        """Define o ID do usuário para filtrar operações."""
        self.user_id = user_id
    
    def _drop_and_create_table(self):
        """Recria a tabela para aplicar as alterações no schema."""
        # Primeiro, verifica se a tabela existe
        cursor = self.conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='pagamentos'
        """)
        if cursor.fetchone():
            # Verifica se já tem a coluna user_id
            cursor = self.conn.execute("PRAGMA table_info(pagamentos)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'user_id' not in columns:
                # Se não tem user_id, dropa a tabela (dados incompatíveis)
                self.conn.execute("DROP TABLE pagamentos")
                self.conn.commit()
                dados_antigos = []
            else:
                # Se já tem user_id, mantém os dados
                cursor = self.conn.execute("SELECT * FROM pagamentos")
                dados_antigos = cursor.fetchall()
                self.conn.execute("DROP TABLE pagamentos")
                self.conn.commit()
        else:
            dados_antigos = []

        # Cria a nova tabela com user_id
        query = """
        CREATE TABLE pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            vencimento TEXT,
            forma_pagamento TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        self.conn.execute(query)
        
        # Restaura os dados antigos se tiverem user_id
        if dados_antigos and len(dados_antigos[0]) >= 5:
            self.conn.executemany(
                "INSERT INTO pagamentos (id, user_id, nome, vencimento, forma_pagamento) VALUES (?, ?, ?, ?, ?)",
                dados_antigos
            )
        
        self.conn.commit()
    
    def add_pagamento(self, pagamento):
        """Adiciona um novo pagamento ao banco."""
        if self.user_id is None:
            raise ValueError("user_id não definido no PagamentosDAO")
        
        query = """
            INSERT INTO pagamentos (user_id, nome, vencimento, forma_pagamento)
            VALUES (?, ?, ?, ?)
        """
        cursor = self.conn.execute(
            query,
            (
                self.user_id,
                pagamento.nome,
                pagamento.vencimento.isoformat() if pagamento.vencimento else None,
                pagamento.forma_de_pagamento.value
            )
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_pagamentos(self):
        """Retorna todos os pagamentos do usuário ordenados por data de vencimento."""
        if self.user_id is None:
            raise ValueError("user_id não definido no PagamentosDAO")
        
        from mvc.models.pagamentos_model import PagamentoModel
        from mvc.models.forma_pagamento_enum import FormaPagamento
        from datetime import datetime

        cursor = self.conn.execute(
            """
            SELECT id, nome, vencimento, forma_pagamento
            FROM pagamentos
            WHERE user_id = ?
            ORDER BY vencimento
            """,
            (self.user_id,)
        )
        
        pagamentos = []
        for row in cursor.fetchall():
            # Converte a data apenas se não for None
            vencimento = datetime.fromisoformat(row[2]).date() if row[2] else None
            pagamento = PagamentoModel(
                nome=row[1],
                vencimento=vencimento,
                forma_de_pagamento=FormaPagamento(row[3])
            )
            setattr(pagamento, 'id', row[0])  # Adiciona o ID ao objeto
            pagamentos.append(pagamento)
        
        return pagamentos
    
    def update_pagamento(self, pagamento_id, pagamento):
        """Atualiza um pagamento existente."""
        if self.user_id is None:
            raise ValueError("user_id não definido no PagamentosDAO")
        
        query = """
            UPDATE pagamentos
            SET nome = ?, vencimento = ?, forma_pagamento = ?
            WHERE id = ? AND user_id = ?
        """
        self.conn.execute(
            query,
            (
                pagamento.nome,
                pagamento.vencimento.isoformat() if pagamento.vencimento else None,
                pagamento.forma_de_pagamento.value,
                pagamento_id,
                self.user_id
            )
        )
        self.conn.commit()
    
    def delete_pagamento(self, pagamento_id):
        """Remove um pagamento do banco."""
        if self.user_id is None:
            raise ValueError("user_id não definido no PagamentosDAO")
        
        self.conn.execute(
            "DELETE FROM pagamentos WHERE id = ? AND user_id = ?",
            (pagamento_id, self.user_id)
        )
        self.conn.commit()

class AssinaturasDAO:
    """DAO para gerenciar assinaturas no banco de dados."""
    
    def __init__(self, db_file="database.sqlite"):
        self.db_file = db_file
        with sqlite3.connect(self.db_file) as conn:
            self._create_table(conn)
            self._create_compartilhamentos_table(conn)
    
    def _create_table(self, conn):
        query = """
        CREATE TABLE IF NOT EXISTS assinaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            data_vencimento TEXT NOT NULL,
            valor REAL NOT NULL,
            periodicidade TEXT NOT NULL,
            tag TEXT NOT NULL,
            forma_pagamento TEXT NOT NULL,
            usuario_compartilhado TEXT,
            login TEXT,
            senha TEXT,
            favorito INTEGER DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Ativo',
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        conn.execute(query)
        conn.commit()
        
        # Ensure favorito column exists in existing databases
        self._ensure_favorito_column(conn)
        self._ensure_status_column(conn)
        self._ensure_created_at_column(conn)
    
    def _ensure_favorito_column(self, conn):
        """Adiciona coluna favorito se não existir."""
        cur = conn.execute("PRAGMA table_info(assinaturas)")
        cols = {row[1] for row in cur.fetchall()}
        if "favorito" not in cols:
            conn.execute(
                "ALTER TABLE assinaturas ADD COLUMN favorito INTEGER DEFAULT 0"
            )
            conn.commit()
    
    def _ensure_status_column(self, conn):
        """Adiciona coluna status se não existir."""
        cur = conn.execute("PRAGMA table_info(assinaturas)")
        cols = {row[1] for row in cur.fetchall()}
        if "status" not in cols:
            conn.execute(
                "ALTER TABLE assinaturas ADD COLUMN status TEXT NOT NULL DEFAULT 'Ativo'"
            )
            conn.commit()
    
    def _ensure_created_at_column(self, conn):
        """Adiciona coluna created_at se não existir."""
        cur = conn.execute("PRAGMA table_info(assinaturas)")
        cols = {row[1] for row in cur.fetchall()}
        if "created_at" not in cols:
            # SQLite não permite DEFAULT CURRENT_TIMESTAMP em ALTER TABLE
            # Usa uma data fixa como fallback para registros antigos
            conn.execute(
                "ALTER TABLE assinaturas ADD COLUMN created_at TEXT"
            )
            # Atualiza registros existentes com a data atual
            conn.execute(
                "UPDATE assinaturas SET created_at = ? WHERE created_at IS NULL",
                (datetime.now().isoformat(),)
            )
            conn.commit()
    
    def _create_compartilhamentos_table(self, conn):
        """Cria tabela para gerenciar compartilhamentos de assinaturas."""
        query = """
        CREATE TABLE IF NOT EXISTS assinaturas_compartilhadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assinatura_id INTEGER NOT NULL,
            user_id_proprietario INTEGER NOT NULL,
            user_id_compartilhado INTEGER NOT NULL,
            compartilhado_em TEXT NOT NULL,
            FOREIGN KEY (assinatura_id) REFERENCES assinaturas (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id_proprietario) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id_compartilhado) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(assinatura_id, user_id_compartilhado)
        )
        """
        conn.execute(query)
        conn.commit()
    
    def adicionar_assinatura(self, assinatura):
        """Adiciona uma nova assinatura ao banco."""
        query = """
            INSERT INTO assinaturas 
            (user_id, nome, data_vencimento, valor, periodicidade, tag, 
             forma_pagamento, usuario_compartilhado, login, senha, favorito, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.execute(
                query,
                (
                    assinatura.user_id,
                    assinatura.nome,
                    assinatura.data_vencimento,
                    assinatura.valor,
                    assinatura.periodicidade,
                    assinatura.tag,
                    assinatura.forma_pagamento,
                    assinatura.usuario_compartilhado,
                    assinatura.login,
                    assinatura.senha,
                    assinatura.favorito,
                    assinatura.status.value if hasattr(assinatura, 'status') else 'Ativo',
                    assinatura.created_at if hasattr(assinatura, 'created_at') else datetime.now().isoformat()
                )
            )
            conn.commit()
            return cursor.lastrowid
    
    def obter_assinaturas_por_usuario(self, user_id: int) -> List:
        """Retorna todas as assinaturas de um usuário, favoritas primeiro."""
        from mvc.models.assinaturas_model import Assinatura
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.execute(
                """
                SELECT id, user_id, nome, data_vencimento, valor, periodicidade, 
                       tag, forma_pagamento, usuario_compartilhado, login, senha, favorito, status, created_at
                FROM assinaturas 
                WHERE user_id = ?
                ORDER BY favorito DESC, data_vencimento
                """,
                (user_id,)
            )
            
            assinaturas = []
            for row in cursor.fetchall():
                assinatura = Assinatura(
                    nome=row[2],
                    data_vencimento=row[3],
                    valor=row[4],
                    periodicidade=row[5],
                    tag=row[6],
                    forma_pagamento=row[7],
                    usuario_compartilhado=row[8],
                    login=row[9],
                    senha=row[10],
                    favorito=row[11],
                    assinatura_id=row[0],
                    user_id=row[1],
                    status=row[12] if len(row) > 12 else 'Ativo',
                    created_at=row[13] if len(row) > 13 else None
                )
                assinaturas.append(assinatura)
            
            return assinaturas
    
    def alternar_favorito(self, assinatura_id: int):
        """Alterna o status de favorito."""
        with sqlite3.connect(self.db_file) as conn:
            # Get current status
            cursor = conn.execute(
                "SELECT favorito FROM assinaturas WHERE id = ?",
                (assinatura_id,)
            )
            row = cursor.fetchone()
            if row:
                new_status = 0 if row[0] == 1 else 1
                conn.execute(
                    "UPDATE assinaturas SET favorito = ? WHERE id = ?",
                    (new_status, assinatura_id)
                )
                conn.commit()
    
    def deletar_assinatura(self, assinatura_id: int):
        """Remove uma assinatura do banco."""
        with sqlite3.connect(self.db_file) as conn:
            conn.execute(
                "DELETE FROM assinaturas WHERE id = ?",
                (assinatura_id,)
            )
            conn.commit()
    
    def atualizar_assinatura(self, assinatura):
        """Atualiza uma assinatura existente."""
        query = """
            UPDATE assinaturas
            SET nome = ?, data_vencimento = ?, valor = ?, periodicidade = ?,
                tag = ?, forma_pagamento = ?, usuario_compartilhado = ?,
                login = ?, senha = ?, favorito = ?, status = ?
            WHERE id = ?
        """
        with sqlite3.connect(self.db_file) as conn:
            conn.execute(
                query,
                (
                    assinatura.nome,
                    assinatura.data_vencimento,
                    assinatura.valor,
                    assinatura.periodicidade,
                    assinatura.tag,
                    assinatura.forma_pagamento,
                    assinatura.usuario_compartilhado,
                    assinatura.login,
                    assinatura.senha,
                    assinatura.favorito,
                    assinatura.status.value if hasattr(assinatura, 'status') else 'Ativo',
                    assinatura.id
                )
            )
            conn.commit()
    
    def compartilhar_assinatura(self, assinatura_id: int, user_id_proprietario: int, user_id_compartilhado: int):
        """
        Compartilha uma assinatura com outro usuário.
        
        Args:
            assinatura_id: ID da assinatura
            user_id_proprietario: ID do proprietário
            user_id_compartilhado: ID do usuário que receberá acesso readonly
        """
        with sqlite3.connect(self.db_file) as conn:
            # Primeiro remove compartilhamento existente (se houver)
            conn.execute(
                "DELETE FROM assinaturas_compartilhadas WHERE assinatura_id = ? AND user_id_compartilhado = ?",
                (assinatura_id, user_id_compartilhado)
            )
            
            # Depois insere o novo compartilhamento
            conn.execute(
                """
                INSERT INTO assinaturas_compartilhadas 
                (assinatura_id, user_id_proprietario, user_id_compartilhado, compartilhado_em)
                VALUES (?, ?, ?, ?)
                """,
                (assinatura_id, user_id_proprietario, user_id_compartilhado, datetime.now().isoformat())
            )
            conn.commit()
            return True
    
    def remover_compartilhamento(self, assinatura_id: int, user_id_compartilhado: int):
        """Remove um compartilhamento."""
        with sqlite3.connect(self.db_file) as conn:
            conn.execute(
                "DELETE FROM assinaturas_compartilhadas WHERE assinatura_id = ? AND user_id_compartilhado = ?",
                (assinatura_id, user_id_compartilhado)
            )
            conn.commit()
    
    def obter_assinaturas_compartilhadas_comigo(self, user_id: int) -> List:
        """
        Retorna assinaturas que foram compartilhadas COMIGO (readonly).
        
        Args:
            user_id: ID do usuário que recebeu o compartilhamento
            
        Returns:
            Lista de assinaturas compartilhadas (com flag is_readonly=True)
        """
        from mvc.models.assinaturas_model import Assinatura
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.execute(
                """
                SELECT a.id, a.user_id, a.nome, a.data_vencimento, a.valor, a.periodicidade, 
                       a.tag, a.forma_pagamento, a.usuario_compartilhado, a.login, a.senha, 
                       a.favorito, a.status, a.created_at
                FROM assinaturas a
                INNER JOIN assinaturas_compartilhadas ac ON a.id = ac.assinatura_id
                WHERE ac.user_id_compartilhado = ?
                ORDER BY a.data_vencimento
                """,
                (user_id,)
            )
            
            assinaturas = []
            for row in cursor.fetchall():
                assinatura = Assinatura(
                    nome=row[2],
                    data_vencimento=row[3],
                    valor=row[4],
                    periodicidade=row[5],
                    tag=row[6],
                    forma_pagamento=row[7],
                    usuario_compartilhado=row[8],
                    login=row[9],
                    senha=row[10],
                    favorito=row[11],
                    assinatura_id=row[0],
                    user_id=row[1],
                    status=row[12] if len(row) > 12 else 'Ativo',
                    created_at=row[13] if len(row) > 13 else None
                )
                assinatura.is_readonly = True  # Marca como apenas leitura
                assinaturas.append(assinatura)
            
            return assinaturas

class ContratosDAO:
    """DAO para gerenciar contratos no banco de dados."""
    
    def __init__(self, db_file="database.sqlite"):
        self.conn = sqlite3.connect(db_file)
        self._create_table()
        self._migrate_schema()
        self._ensure_status_column()
        
    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS contratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            data_vencimento TEXT NOT NULL,
            valor REAL NOT NULL,
            periodicidade TEXT NOT NULL,
            tag TEXT NOT NULL,
            usuario_compartilhado TEXT,
            favorito INTEGER DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Ativo',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        self.conn.execute(query)
        self.conn.commit()
        self._ensure_favorito_column()
    
    def _ensure_favorito_column(self):
        """Adiciona coluna favorito se não existir."""
        cur = self.conn.execute("PRAGMA table_info(contratos)")
        cols = {row[1] for row in cur.fetchall()}
        if "favorito" not in cols:
            self.conn.execute(
                "ALTER TABLE contratos ADD COLUMN favorito INTEGER DEFAULT 0"
            )
            self.conn.commit()
    
    def _ensure_status_column(self):
        """Adiciona coluna status se não existir."""
        cur = self.conn.execute("PRAGMA table_info(contratos)")
        cols = {row[1] for row in cur.fetchall()}
        if "status" not in cols:
            self.conn.execute(
                "ALTER TABLE contratos ADD COLUMN status TEXT NOT NULL DEFAULT 'Ativo'"
            )
            self.conn.commit()
    
    def _migrate_schema(self):
        """Migra schema antigo removendo colunas forma_pagamento/login/senha se existirem."""
        try:
            cur = self.conn.execute("PRAGMA table_info(contratos)")
            cols = [row[1] for row in cur.fetchall()]
            if not cols:
                return
            # Se tabela possui quaisquer colunas antigas, recria com schema novo
            if any(c in cols for c in ("forma_pagamento", "login", "senha")):
                self.conn.execute(
                    """
                    CREATE TABLE contratos_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        nome TEXT NOT NULL,
                        data_vencimento TEXT NOT NULL,
                        valor REAL NOT NULL,
                        periodicidade TEXT NOT NULL,
                        tag TEXT NOT NULL,
                        usuario_compartilhado TEXT,
                        favorito INTEGER DEFAULT 0,
                        status TEXT NOT NULL DEFAULT 'Ativo',
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                    """
                )
                self.conn.execute(
                    """
                    INSERT INTO contratos_new (
                        id, user_id, nome, data_vencimento, valor, periodicidade, tag, usuario_compartilhado, favorito, status
                    )
                    SELECT 
                        id, user_id, nome, data_vencimento, valor, periodicidade, tag, usuario_compartilhado, COALESCE(favorito, 0), 'Ativo'
                    FROM contratos
                    """
                )
                self.conn.execute("DROP TABLE contratos")
                self.conn.execute("ALTER TABLE contratos_new RENAME TO contratos")
                self.conn.commit()
        except Exception:
            # Se algo falhar, não quebrar app; mantém tabela como está
            pass
    
    def add_contrato(self, contrato):
        """Adiciona um novo contrato ao banco."""
        cursor = self.conn.execute(
            """
            INSERT INTO contratos (
                user_id, nome, data_vencimento, valor, periodicidade, tag, usuario_compartilhado, favorito, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                contrato.user_id,
                contrato.nome,
                contrato.data_vencimento,
                contrato.valor,
                contrato.periodicidade if isinstance(contrato.periodicidade, str) else contrato.periodicidade.value,
                contrato.tag if isinstance(contrato.tag, str) else contrato.tag.value,
                contrato.usuario_compartilhado,
                1 if getattr(contrato, "favorito", False) else 0,
                contrato.status.value if hasattr(contrato, 'status') else 'Ativo',
            ),
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_contratos_by_user(self, user_id: int) -> List:
        """Retorna todos os contratos de um usuário, favoritos primeiro."""
        cursor = self.conn.execute(
            """
            SELECT id, user_id, nome, data_vencimento, valor, periodicidade, tag, usuario_compartilhado, favorito, status
            FROM contratos
            WHERE user_id = ?
            ORDER BY favorito DESC, id DESC
            """,
            (user_id,),
        )
        rows = cursor.fetchall()
        return [
            {
                "id": r[0],
                "user_id": r[1],
                "nome": r[2],
                "data_vencimento": r[3],
                "valor": r[4],
                "periodicidade": r[5],
                "tag": r[6],
                "usuario_compartilhado": r[7],
                "favorito": bool(r[8]),
                "status": r[9],
            }
            for r in rows
        ]
    
    def toggle_favorito(self, contrato_id: int):
        """Alterna o status de favorito."""
        cursor = self.conn.execute(
            "SELECT favorito FROM contratos WHERE id = ?",
            (contrato_id,)
        )
        row = cursor.fetchone()
        if row is not None:
            new_status = 0 if row[0] == 1 else 1
            self.conn.execute(
                "UPDATE contratos SET favorito = ? WHERE id = ?",
                (new_status, contrato_id)
            )
            self.conn.commit()
    
    def delete_contrato(self, contrato_id: int):
        """Remove um contrato do banco."""
        self.conn.execute(
            "DELETE FROM contratos WHERE id = ?",
            (contrato_id,)
        )
        self.conn.commit()
    
    def update_contrato(self, contrato):
        """Atualiza um contrato existente."""
        self.conn.execute(
            """
            UPDATE contratos
            SET nome = ?, data_vencimento = ?, valor = ?, periodicidade = ?, tag = ?, usuario_compartilhado = ?, favorito = ?, status = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                contrato.nome,
                contrato.data_vencimento,
                contrato.valor,
                contrato.periodicidade if isinstance(contrato.periodicidade, str) else contrato.periodicidade.value,
                contrato.tag if isinstance(contrato.tag, str) else contrato.tag.value,
                contrato.usuario_compartilhado,
                1 if getattr(contrato, "favorito", False) else 0,
                contrato.status.value if hasattr(contrato, 'status') else 'Ativo',
                contrato.id,
                contrato.user_id,
            ),
        )
        self.conn.commit()
