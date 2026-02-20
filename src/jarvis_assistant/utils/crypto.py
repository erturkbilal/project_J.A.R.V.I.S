from __future__ import annotations

from cryptography.fernet import Fernet


class CryptoService:
    def __init__(self, key: str | None = None) -> None:
        if key:
            self.key = key.encode()
        else:
            self.key = Fernet.generate_key()
        self._fernet = Fernet(self.key)

    def encrypt(self, plain_text: str) -> str:
        return self._fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, cipher_text: str) -> str:
        return self._fernet.decrypt(cipher_text.encode()).decode()
