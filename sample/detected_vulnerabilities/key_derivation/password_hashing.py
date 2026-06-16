"""
Password and key derivation examples
Covers PBKDF2, bcrypt, scrypt, and Argon2 patterns.
"""

import hashlib
from Crypto.Protocol.KDF import PBKDF2, scrypt as crypto_scrypt
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

try:
    import bcrypt
except ImportError:
    bcrypt = None

try:
    import argon2
except ImportError:
    argon2 = None

# --- Legacy: MD5 and SHA-1 password hashing (DO NOT USE) ---

def hash_password_md5(password: str) -> str:
    """MD5 password hash - BROKEN, vulnerable to collision attacks."""
    return hashlib.md5(password.encode()).hexdigest()

def hash_password_sha1(password: str) -> str:
    """SHA-1 password hash - Deprecated, vulnerable to collision attacks."""
    return hashlib.sha1(password.encode()).hexdigest()

# --- Weak: Unsalted SHA-256 ---

def hash_password_unsalted_sha256(password: str) -> str:
    """Unsalted SHA-256 - No salt means rainbow tables work."""
    return hashlib.sha256(password.encode()).hexdigest()

# --- Better: SHA-256 with salt ---

def hash_password_salted_sha256(password: str, salt: bytes = None) -> tuple:
    """SHA-256 with salt - Better but still not recommended for passwords."""
    if salt is None:
        salt = get_random_bytes(32)
    h = hashlib.sha256(salt + password.encode()).hexdigest()
    return h, salt.hex()

# --- Good: PBKDF2 ---

def hash_password_pbkdf2(password: str, salt: bytes = None, iterations: int = 100000) -> tuple:
    """PBKDF2 key derivation - Good but slow by design (iterations)."""
    if salt is None:
        salt = get_random_bytes(32)
    key = PBKDF2(password, salt, dkLen=32, count=iterations, hmac_hash_module=SHA256)
    return key.hex(), salt.hex()

def verify_password_pbkdf2(password: str, stored_key: str, salt: str, iterations: int = 100000) -> bool:
    """Verify PBKDF2 password."""
    key = PBKDF2(password, bytes.fromhex(salt), dkLen=32, count=iterations, hmac_hash_module=SHA256)
    return key.hex() == stored_key

# --- Better: scrypt ---

def hash_password_scrypt(password: str, salt: bytes = None) -> tuple:
    """scrypt key derivation - Better security properties than PBKDF2."""
    if salt is None:
        salt = get_random_bytes(32)
    key = crypto_scrypt(password, salt, 32, N=16384, r=8, p=1)
    return key.hex(), salt.hex()

# --- Excellent: bcrypt ---

def hash_password_bcrypt(password: str) -> str:
    """bcrypt password hashing - Excellent for password storage."""
    if bcrypt is None:
        return None
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password_bcrypt(password: str, hashed: str) -> bool:
    """Verify bcrypt password."""
    if bcrypt is None:
        return False
    return bcrypt.checkpw(password.encode(), hashed.encode())

# --- Excellent: Argon2 ---

def hash_password_argon2(password: str) -> str:
    """Argon2 password hashing - State-of-the-art for password storage."""
    if argon2 is None:
        return None
    ph = argon2.PasswordHasher()
    return ph.hash(password)

def verify_password_argon2(password: str, hashed: str) -> bool:
    """Verify Argon2 password."""
    if argon2 is None:
        return False
    try:
        ph = argon2.PasswordHasher()
        ph.verify(hashed, password)
        return True
    except Exception:
        return False

# --- HMAC examples ---

import hmac

def compute_hmac_sha256(message: bytes, key: bytes) -> str:
    """HMAC-SHA256 for message authentication."""
    h = hmac.new(key, message, hashlib.sha256)
    return h.hexdigest()

def verify_hmac_sha256(message: bytes, key: bytes, signature: str) -> bool:
    """Verify HMAC-SHA256 signature."""
    expected = compute_hmac_sha256(message, key)
    return hmac.compare_digest(expected, signature)

# --- Summary of recommendations ---
def get_recommendations() -> dict:
    """Return password hashing recommendations by use case."""
    return {
        "web_applications": "Use Argon2 or bcrypt with 12+ rounds",
        "legacy_systems": "Migrate from MD5/SHA1 to PBKDF2 at minimum",
        "modern_backends": "Argon2id (resistant to GPU/ASIC attacks)",
        "password_verification": "Always use constant-time comparison (hmac.compare_digest)",
        "never_use": ["MD5", "SHA1", "SHA256 without salt"],
    }
