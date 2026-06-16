"""
Symmetric key manager
Encrypt/decrypt sensitive data at rest.
"""

import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16

# --- Key derivation ---

def derive_aes_key(master_password: str, salt: bytes) -> bytes:
    """Derive an AES key from a master password."""
    return hashlib.sha256(master_password.encode() + salt).digest()  # 256-bit key

# --- AES encryption ---

def encrypt_sensitive_data(data: bytes, key: bytes) -> tuple[bytes, bytes]:
    """Encrypt sensitive data with AES-CBC."""
    cipher = AES.new(key, AES.MODE_CBC)
    padded = _pad(data)
    return cipher.encrypt(padded), cipher.iv

def decrypt_sensitive_data(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt data with AES-CBC."""
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return _unpad(cipher.decrypt(ciphertext))

# --- Utilities ---

def _pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def _unpad(data: bytes) -> bytes:
    return data[:-data[-1]]

def generate_session_key() -> bytes:
    return get_random_bytes(32)  # AES-256

def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()
