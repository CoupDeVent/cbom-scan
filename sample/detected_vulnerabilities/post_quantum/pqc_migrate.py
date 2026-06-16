"""
Post-Quantum migration module (v2 - PQC Ready)
Gradual replacement of vulnerable primitives with NIST PQC standards.
"""

import oqs  # liboqs-python - Open Quantum Safe

# --- Key encapsulation mechanism (KEM) ---

def kem_keygen() -> tuple[bytes, bytes]:
    """Generate an ML-KEM-768 key pair (NIST FIPS 203)."""
    with oqs.KeyEncapsulation("ML-KEM-768") as kem:
        public_key = kem.generate_keypair()
        secret_key = kem.export_secret_key()
    return public_key, secret_key

def kem_encapsulate(public_key: bytes) -> tuple[bytes, bytes]:
    """Encapsulate a shared key with ML-KEM-768."""
    with oqs.KeyEncapsulation("ML-KEM-768") as kem:
        ciphertext, shared_secret = kem.encap_secret(public_key)
    return ciphertext, shared_secret

def kem_decapsulate(ciphertext: bytes, secret_key: bytes) -> bytes:
    """Decapsulate to recover the shared key."""
    with oqs.KeyEncapsulation("ML-KEM-768", secret_key) as kem:
        return kem.decap_secret(ciphertext)

# --- Post-quantum digital signature (DSA) ---

def sign_keygen() -> tuple[bytes, bytes]:
    """Generate an ML-DSA-65 key pair (NIST FIPS 204)."""
    with oqs.Signature("ML-DSA-65") as signer:
        public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()
    return public_key, secret_key

def pqc_sign(message: bytes, secret_key: bytes) -> bytes:
    """Sign a message with ML-DSA-65."""
    with oqs.Signature("ML-DSA-65", secret_key) as signer:
        return signer.sign(message)

def pqc_verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
    """Verify an ML-DSA-65 signature."""
    with oqs.Signature("ML-DSA-65") as verifier:
        return verifier.verify(message, signature, public_key)

# --- Hybrid mode (recommended transition approach) ---

def hybrid_kem_exchange(classical_secret: bytes, pqc_shared: bytes) -> bytes:
    """Combine a classical X25519 secret and an ML-KEM secret for transition."""
    import hashlib
    return hashlib.sha256(classical_secret + pqc_shared).digest()
