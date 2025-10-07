import hashlib
import os

class Usuario:
    def __init__(self, nome: str, email: str, senha: str, user_id: int = None,  limite_assinaturas: float = 0.0, limite_contratos: float = 0.0):
        self.id = user_id
        self.nome = nome
        self.email = email
        self.senha_hash = self._hash_password(senha)
        self._limite_assinaturas = limite_assinaturas
        self._limite_contratos = limite_contratos

    # ---------------- HASH PASSWORD ----------------
    def _hash_password(self, senha: str) -> str:
        """Cria um hash seguro usando sha256 + salt"""
        salt = os.urandom(32)  # salt aleatório de 32 bytes
        pwdhash = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, 100000)
        # Salva salt + hash juntos
        return salt.hex() + pwdhash.hex()

    # ---------------- VERIFY PASSWORD ----------------
    def verify_password(self, senha: str) -> bool:
        """Verifica se a senha fornecida bate com o hash salvo"""
        salt_hex = self.senha_hash[:64]  # primeiros 32 bytes em hex
        pwdhash_hex = self.senha_hash[64:]  # resto do hash
        salt = bytes.fromhex(salt_hex)
        pwdhash = bytes.fromhex(pwdhash_hex)
        check_hash = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, 100000)
        return check_hash.hex() == pwdhash_hex

    # ---------------- REPRESENTAÇÃO ----------------
    def __repr__(self):
        return f"<Usuario id={self.id} nome={self.nome} email={self.email}>"
    
    # ---------- Propriedade para limite_assinaturas ------------

    @property
    def limite_assinaturas(self):
        # Getter → retorna o valor do limite de assinaturas
        return self._limite_assinaturas

    @limite_assinaturas.setter
    def limite_assinaturas(self, valor: float):
        # Setter → valida o valor antes de atribuir
        if valor < 0:
            # Se for negativo, gera erro
            raise ValueError("O limite de assinaturas deve ser positivo.")
        # Se for válido, atualiza o atributo
        self._limite_assinaturas = valor

   # ---------- Propriedade para limite_contratos ------------

    @property
    def limite_contratos(self):
        # Getter → retorna o valor do limite de contratos
        return self._limite_contratos

    @limite_contratos.setter
    def limite_contratos(self, valor: float):
        # Setter → valida o valor antes de atribuir
        if valor < 0:
            # Se for negativo, gera erro
            raise ValueError("O limite de contratos deve ser positivo.")
        # Se for válido, atualiza o atributo
        self._limite_contratos = valor
