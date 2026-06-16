"""
Authentication service (legacy)
Module managing key generation, signature creation, and password hashing.
"""

import hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA1

# --- RSA key generation ---

def generate_rsa_keypair():
    """Generate an RSA key pair for signing auth tokens."""
    key = RSA.generate(2048)
    return key.export_key(), key.publickey().export_key()

# --- Token signing ---

def sign_auth_token(token_data: bytes, private_key_pem: bytes) -> bytes:
    """Sign a token using RSA + SHA-1."""
    key = RSA.import_key(private_key_pem)
    h = SHA1.new(token_data)           # SHA-1 deprecated!
    return pkcs1_15.new(key).sign(h)

# --- Password hashing ---

def hash_password_legacy(password: str) -> str:
    """Hash a password using a legacy method."""
    return hashlib.md5(password.encode()).hexdigest()  # MD5 broken!

def hash_password(password: str, salt: str) -> str:
    """Hash a password with salt using an improved method."""
    return hashlib.sha256((password + salt).encode()).hexdigest()

# --- Token verification ---

def verify_token(token_data: bytes, signature: bytes, public_key_pem: bytes) -> bool:
    key = RSA.import_key(public_key_pem)
    h = SHA1.new(token_data)
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False
