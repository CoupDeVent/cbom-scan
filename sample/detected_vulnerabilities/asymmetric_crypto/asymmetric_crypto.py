"""
Asymmetric cryptography examples
Covers RSA, DSA, ECC (ECDSA), Ed25519, X25519, and Diffie-Hellman patterns.
"""

from Crypto.PublicKey import RSA, ECC, DSA
from Crypto.Signature import pkcs1_15, dss
from Crypto.Cipher import PKCS1_OAEP
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, ed25519, x25519, dh
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.backends import default_backend

# --- RSA Examples (quantum-vulnerable, Shor's algorithm breakable) ---

def generate_rsa_keypair_pycryptodome(bits: int = 2048) -> tuple:
    """Generate RSA key pair using PyCryptodome."""
    key = RSA.generate(bits)
    return key.export_key(), key.publickey().export_key()

def sign_with_rsa_pkcs1v15(data: bytes, private_key_pem: bytes) -> bytes:
    """Sign data with RSA using PKCS#1 v1.5."""
    key = RSA.import_key(private_key_pem)
    h = __import__('Crypto.Hash.SHA256', fromlist=['new']).new(data)
    signer = pkcs1_15.new(key)
    return signer.sign(h)

def encrypt_with_rsa_oaep(data: bytes, public_key_pem: bytes) -> bytes:
    """Encrypt with RSA-OAEP."""
    key = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(data)

def generate_rsa_keypair_cryptography(bits: int = 2048):
    """Generate RSA key pair using cryptography library."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=bits,
        backend=default_backend()
    )
    return private_key, private_key.public_key()

def sign_with_rsa_pss(data: bytes, private_key) -> bytes:
    """Sign data with RSA using PSS (better padding than PKCS#1 v1.5)."""
    return private_key.sign(
        data,
        asym_padding.PSS(
            mgf=asym_padding.MGF1(hashes.SHA256()),
            salt_length=asym_padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

# --- DSA Examples (quantum-vulnerable) ---

def generate_dsa_keypair() -> tuple:
    """Generate DSA key pair (use ECC instead - faster, smaller)."""
    key = DSA.generate(1024)
    return key.export_key(), key.publickey().export_key()

# --- ECC Examples (quantum-vulnerable, but more efficient than RSA) ---

def generate_ecc_keypair_pycryptodome(curve: str = 'P-256') -> tuple:
    """Generate ECC key pair using PyCryptodome."""
    key = ECC.generate(curve=curve)
    return key.export_key(), key.public_key.export_key()

def generate_ecc_keypair_cryptography() -> tuple:
    """Generate ECC key pair using cryptography library."""
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    return private_key, private_key.public_key()

def sign_with_ecdsa(data: bytes, private_key) -> bytes:
    """Sign data with ECDSA."""
    return private_key.sign(data, ec.ECDSA(hashes.SHA256()))

def verify_ecdsa(data: bytes, signature: bytes, public_key) -> bool:
    """Verify ECDSA signature."""
    try:
        public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
        return True
    except Exception:
        return False

# --- Post-Quantum Safe: Ed25519 ---

def generate_ed25519_keypair():
    """Generate Ed25519 key pair (post-quantum safe for signatures)."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    return private_key, private_key.public_key()

def sign_with_ed25519(data: bytes, private_key) -> bytes:
    """Sign data with Ed25519."""
    return private_key.sign(data)

def verify_ed25519(data: bytes, signature: bytes, public_key) -> bool:
    """Verify Ed25519 signature."""
    try:
        public_key.verify(signature, data)
        return True
    except Exception:
        return False

# --- Post-Quantum Safe: X25519 (Key Exchange) ---

def generate_x25519_keypair():
    """Generate X25519 key pair (post-quantum safe for key exchange)."""
    private_key = x25519.X25519PrivateKey.generate()
    return private_key, private_key.public_key()

def exchange_x25519(private_key, peer_public_key: bytes) -> bytes:
    """Perform X25519 key exchange."""
    return private_key.exchange(peer_public_key)

# --- Diffie-Hellman Key Exchange (quantum-vulnerable) ---

def generate_dh_parameters() -> tuple:
    """Generate DH parameters (slow, use alternatives)."""
    parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
    return parameters

def dh_key_exchange(parameters):
    """Generate DH private key."""
    private_key = parameters.generate_private_key()
    return private_key, private_key.public_key()

# --- Hybrid Approach: Classical + Post-Quantum ---

def hybrid_kem_setup():
    """Set up hybrid key encapsulation using X25519 + Post-quantum KEM."""
    # Classical: X25519
    classical_private = x25519.X25519PrivateKey.generate()
    
    # Post-quantum would use ML-KEM (requires liboqs or similar)
    # For this example, showing the pattern:
    # pqc_private, pqc_public = kem_keygen()  # ML-KEM
    
    return {
        "classical": classical_private,
        "classical_public": classical_private.public_key().public_bytes_raw(),
        # "pqc": pqc_private,
        # "pqc_public": pqc_public,
        "note": "Combine classical and post-quantum for long-term security"
    }

# --- Recommendations ---

def get_asymmetric_recommendations() -> dict:
    """Return asymmetric cryptography recommendations."""
    return {
        "signing": {
            "modern": "Ed25519 (fastest, quantum-safe for signatures)",
            "traditional": "ECDSA with NIST curves or RSA with 2048+ bits",
            "avoid": "DSA, SHA1withRSA"
        },
        "key_exchange": {
            "modern": "X25519 (efficient, quantum-safe)",
            "traditional": "ECDH with NIST curves or DH (slow)",
            "post_quantum": "ML-KEM (via liboqs)"
        },
        "encryption": {
            "best": "Use symmetric encryption (AES-GCM) with hybrid key exchange",
            "rsa": "RSA-OAEP with SHA-256 minimum",
            "avoid": "RSA with PKCS#1 v1.5 padding"
        },
        "quantum_readiness": {
            "now": "Use Ed25519 and X25519",
            "transition": "Implement hybrid classical + PQC",
            "future": "Migrate to ML-DSA for signing, ML-KEM for key exchange"
        }
    }
