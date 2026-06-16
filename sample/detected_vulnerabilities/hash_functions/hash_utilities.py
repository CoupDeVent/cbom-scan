"""
Hash function examples
Covers MD5, SHA-1, SHA-2, SHA-3, BLAKE2 patterns.
"""

import hashlib
from Crypto.Hash import MD5, SHA1, SHA256, SHA512, SHA3_256, SHA3_512, BLAKE2s, BLAKE2b

# --- Vulnerable: MD5 ---

def compute_md5(data: bytes) -> str:
    """MD5 hash - VULNERABLE, collision attacks are practical."""
    h = MD5.new()
    h.update(data)
    return h.hexdigest()

def compute_md5_hashlib(data: bytes) -> str:
    """MD5 via hashlib - Still vulnerable."""
    return hashlib.md5(data).hexdigest()

# --- Vulnerable: SHA-1 ---

def compute_sha1(data: bytes) -> str:
    """SHA-1 hash - Deprecated, collision attacks exist."""
    h = SHA1.new()
    h.update(data)
    return h.hexdigest()

def compute_sha1_hashlib(data: bytes) -> str:
    """SHA-1 via hashlib - Deprecated for cryptographic use."""
    return hashlib.sha1(data).hexdigest()

# --- Secure: SHA-2 family ---

def compute_sha224(data: bytes) -> str:
    """SHA-224 hash - 224-bit output, resistant to Grover's algorithm."""
    return hashlib.sha224(data).hexdigest()

def compute_sha256(data: bytes) -> str:
    """SHA-256 hash - 256-bit output, NIST standard."""
    h = SHA256.new()
    h.update(data)
    return h.hexdigest()

def compute_sha384(data: bytes) -> str:
    """SHA-384 hash - 384-bit output."""
    return hashlib.sha384(data).hexdigest()

def compute_sha512(data: bytes) -> str:
    """SHA-512 hash - 512-bit output, good for long-term security."""
    h = SHA512.new()
    h.update(data)
    return h.hexdigest()

# --- Modern: SHA-3 family ---

def compute_sha3_224(data: bytes) -> str:
    """SHA3-224 hash - 224-bit output, NIST FIPS 202."""
    return hashlib.sha3_224(data).hexdigest()

def compute_sha3_256(data: bytes) -> str:
    """SHA3-256 hash - 256-bit output from Keccak."""
    h = SHA3_256.new()
    h.update(data)
    return h.hexdigest()

def compute_sha3_384(data: bytes) -> str:
    """SHA3-384 hash - 384-bit output."""
    return hashlib.sha3_384(data).hexdigest()

def compute_sha3_512(data: bytes) -> str:
    """SHA3-512 hash - 512-bit output, secure against quantum attacks."""
    h = SHA3_512.new()
    h.update(data)
    return h.hexdigest()

# --- Modern: BLAKE2 family ---

def compute_blake2s(data: bytes) -> str:
    """BLAKE2s hash - 256-bit, fast and secure, optimized for small output."""
    h = BLAKE2s.new()
    h.update(data)
    return h.hexdigest()

def compute_blake2b(data: bytes) -> str:
    """BLAKE2b hash - 512-bit, fastest modern hash function."""
    h = BLAKE2b.new()
    h.update(data)
    return h.hexdigest()

def compute_blake2b_512(data: bytes) -> str:
    """BLAKE2b with 512-bit output."""
    return hashlib.blake2b(data).hexdigest()

# --- Extendable output: SHAKE ---

def compute_shake128(data: bytes, length: int = 32) -> str:
    """SHAKE128 XOF - Variable output length."""
    return hashlib.shake_128(data).hexdigest(length)

def compute_shake256(data: bytes, length: int = 32) -> str:
    """SHAKE256 XOF - Variable output length, more secure."""
    return hashlib.shake_256(data).hexdigest(length)

# --- File hashing with streaming ---

def compute_file_hash_sha256(filepath: str) -> str:
    """Stream-based SHA-256 for large files."""
    sha256_hash = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

# --- Incremental hashing ---

class IncrementalHasher:
    """Helper for incremental hashing."""
    
    def __init__(self, algorithm: str = 'sha256'):
        """Initialize hasher with specified algorithm."""
        self.hasher = hashlib.new(algorithm)
    
    def update(self, data: bytes) -> None:
        """Add data to hash."""
        self.hasher.update(data)
    
    def digest(self) -> str:
        """Get final hash."""
        return self.hasher.hexdigest()

# --- Hash comparison utilities ---

import hmac

def constant_time_hash_compare(hash1: str, hash2: str) -> bool:
    """Compare hashes in constant time to prevent timing attacks."""
    return hmac.compare_digest(hash1, hash2)

# --- Recommendations ---

def get_hash_recommendations() -> dict:
    """Return hash algorithm recommendations."""
    return {
        "never_use": ["MD5", "SHA1"],
        "legacy_support": "SHA256 or SHA512",
        "new_projects": "SHA3-256 or BLAKE2b",
        "file_integrity": "SHA256 or SHA3-256",
        "cryptographic_proof": "SHA3-512 or BLAKE2b",
        "performance_critical": "BLAKE2b (fastest modern algorithm)",
        "quantum_resistant": "SHA3-512 (Grover's algorithm limited impact)",
    }
