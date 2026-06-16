"""
Examples of symmetric encryption implementations
Covers AES, DES, 3DES, Blowfish, RC4, and ChaCha20 patterns.
"""

from Crypto.Cipher import AES, DES, DES3, Blowfish, ARC4, ChaCha20
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# --- Legacy and vulnerable symmetric ciphers ---

def encrypt_with_des(data: bytes, key: bytes, iv: bytes) -> bytes:
    """DES encryption - VULNERABLE! 56-bit key size is broken."""
    cipher = DES.new(key, DES.MODE_CBC, iv)
    return cipher.encrypt(data)

def encrypt_with_3des(data: bytes, key: bytes, iv: bytes) -> bytes:
    """3DES (TripleDES) encryption - Deprecated, vulnerable to Sweet32."""
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    return cipher.encrypt(data)

def encrypt_with_blowfish(data: bytes, key: bytes, iv: bytes) -> bytes:
    """Blowfish encryption - Deprecated, 64-bit block size vulnerable."""
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    return cipher.encrypt(data)

def encrypt_with_rc4(data: bytes, key: bytes) -> bytes:
    """RC4 stream cipher - BROKEN, do not use."""
    cipher = ARC4.new(key)
    return cipher.encrypt(data)

# --- Modern symmetric ciphers (still vulnerable to quantum) ---

def encrypt_with_aes_pycryptodome(data: bytes, key: bytes, iv: bytes) -> bytes:
    """AES encryption via PyCryptodome - good but vulnerable to Grover's algorithm."""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(data)

def encrypt_with_aes_cryptography(data: bytes, key: bytes, iv: bytes) -> bytes:
    """AES encryption via cryptography library (hazmat)."""
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

def encrypt_with_chacha20(data: bytes, key: bytes) -> bytes:
    """ChaCha20 stream cipher - modern but still vulnerable to quantum."""
    cipher = ChaCha20.new(key=key)
    return cipher.encrypt(data)

def encrypt_with_chacha20_cryptography(data: bytes, key: bytes, nonce: bytes) -> bytes:
    """ChaCha20 via cryptography library."""
    cipher = Cipher(
        algorithms.ChaCha20(key, nonce),
        mode=None,
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

# --- Symmetric cipher mode examples ---

def encrypt_aes_ecb(data: bytes, key: bytes) -> bytes:
    """AES in ECB mode - NOT recommended, reveals patterns."""
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)

def encrypt_aes_cbc(data: bytes, key: bytes, iv: bytes) -> bytes:
    """AES in CBC mode - common but requires proper padding."""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(data)

def encrypt_aes_ctr(data: bytes, key: bytes, nonce: bytes) -> bytes:
    """AES in CTR mode - stream cipher mode, good for variable-length data."""
    from Crypto.Util import Counter
    ctr = Counter.new(128, prefix=nonce[:8])
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(data)

def encrypt_aes_gcm(data: bytes, key: bytes, nonce: bytes) -> tuple:
    """AES in GCM mode - authenticated encryption."""
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, tag
