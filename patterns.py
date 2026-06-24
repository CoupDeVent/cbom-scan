#!/usr/bin/env python3
"""
Cryptographic signature dictionary for CBOM scanner (regex-based detection).

Entry structure
----------------
- id              : unique rule identifier (e.g. "PY-001")
- language        : "python" | "java" | "javascript"
- category        : "symmetric" | "asymmetric" | "hash" | "mac" | "kdf" | "pqc"
- algorithm       : detected algorithm or family name
- regex           : pattern to apply (re.search, line by line)
- quantum_impact  : "shor_breakable"  -> breakable by Shor's algorithm
                    "grover_weakened" -> weakened security by Grover's algorithm
                    "already_weak"    -> already deprecated / insecure
                    "quantum_safe"    -> post-quantum algorithm (NIST)
- risk_level      : "critical" | "high" | "medium" | "low" | "info"
- oid             : NIST/ANSI/PKCS OID if standardized, otherwise None
- notes           : context / library description
"""

from collections import Counter

# Field order for each tuple in CRYPTO_PATTERNS_RAW
FIELDS = ("id", "category", "algorithm", "regex", "quantum_impact", "risk_level", "oid", "notes")

CRYPTO_PATTERNS_RAW = {

    # ========================================================================
    # PYTHON
    # ========================================================================
    "python": [
        # --- Symmetric ciphers ---
        ("PY-001", "symmetric", "AES",
         r"from\s+Crypto\.Cipher\s+import\s+AES\b|Crypto\.Cipher\.AES",
         "grover_weakened", "medium", "2.16.840.1.101.3.4.1", "PyCryptodome"),

        ("PY-002", "symmetric", "AES",
         r"cryptography\.hazmat\.primitives\.ciphers\.algorithms.*AES|algorithms\.AES\(",
         "grover_weakened", "medium", "2.16.840.1.101.3.4.1", "lib cryptography (hazmat)"),

        ("PY-003", "symmetric", "AES-128-CBC (via Fernet)",
         r"from\s+cryptography\.fernet\s+import\s+Fernet|\bFernet\s*=\s*Fernet\(",
         "grover_weakened", "medium", None,
         "Fernet uses AES-128-CBC + HMAC-SHA256 with a fixed 128-bit key"),

        ("PY-004", "symmetric", "DES / 3DES",
         r"Crypto\.Cipher\.(DES3?|TripleDES)\b|from\s+Crypto\.Cipher\s+import\s+DES3?\b",
         "already_weak", "critical", None, "PyCryptodome - obsolete"),

        ("PY-005", "symmetric", "Blowfish",
         r"Crypto\.Cipher\.Blowfish|from\s+Crypto\.Cipher\s+import\s+Blowfish",
         "already_weak", "high", None, "64-bit block cipher - vulnerable to Sweet32"),

        ("PY-006", "symmetric", "RC4 / ARC4",
         r"Crypto\.Cipher\.ARC4|from\s+Crypto\.Cipher\s+import\s+ARC4",
         "already_weak", "critical", None, "Broken stream cipher"),

        ("PY-007", "symmetric", "ChaCha20 / ChaCha20-Poly1305",
         r"Crypto\.Cipher\.ChaCha20|algorithms\.ChaCha20\(",
         "grover_weakened", "medium", None, "PyCryptodome / lib cryptography"),

        # --- Asymmetric ---
        ("PY-008", "asymmetric", "RSA",
         r"Crypto\.PublicKey\.RSA|from\s+Crypto\.PublicKey\s+import\s+RSA",
         "shor_breakable", "high", "1.2.840.113549.1.1.1", "PyCryptodome"),

        ("PY-009", "asymmetric", "RSA",
         r"cryptography\.hazmat\.primitives\.asymmetric.*\brsa\b|asymmetric\.rsa\.",
         "shor_breakable", "high", "1.2.840.113549.1.1.1", "lib cryptography"),

        ("PY-010", "asymmetric", "DSA",
         r"Crypto\.PublicKey\.DSA|asymmetric\.dsa\.",
         "shor_breakable", "high", "1.2.840.10040.4.1", ""),

        ("PY-011", "asymmetric", "ECC (ECDSA / ECDH)",
         r"Crypto\.PublicKey\.ECC|asymmetric\.ec\.",
         "shor_breakable", "high", "1.2.840.10045.2.1", ""),

        ("PY-012", "asymmetric", "Ed25519",
         r"asymmetric\.ed25519|Ed25519PrivateKey|Ed25519PublicKey",
         "shor_breakable", "high", "1.3.101.112", ""),

        ("PY-013", "asymmetric", "X25519",
         r"asymmetric\.x25519|X25519PrivateKey|X25519PublicKey",
         "shor_breakable", "high", "1.3.101.110", ""),

        ("PY-014", "asymmetric", "Diffie-Hellman",
         r"asymmetric\.dh\.|DHParameterNumbers",
         "shor_breakable", "high", "1.2.840.113549.1.3.1", ""),

        # --- Hash ---
        ("PY-015", "hash", "MD5",
         r"hashlib\.md5|Crypto\.Hash\.MD5",
         "already_weak", "critical", "1.2.840.113549.2.5", ""),

        ("PY-016", "hash", "SHA-1",
         r"hashlib\.sha1\b|Crypto\.Hash\.SHA1\b",
         "already_weak", "high", "1.3.14.3.2.26", ""),

        ("PY-017", "hash", "SHA-2 (224/256/384/512)",
         r"hashlib\.sha(224|256|384|512)\b",
         "grover_weakened", "medium", "2.16.840.1.101.3.4.2", "Arc OID NIST SHA-2"),

        ("PY-018", "hash", "SHA-3 / SHAKE",
         r"hashlib\.sha3_(224|256|384|512)|hashlib\.shake_(128|256)",
         "grover_weakened", "medium", None, ""),

        ("PY-019", "hash", "BLAKE2 (b/s)",
         r"hashlib\.blake2[bs]",
         "grover_weakened", "medium", None, ""),

        # --- MAC ---
        ("PY-020", "mac", "HMAC",
         r"hmac\.new\(|Crypto\.Hash\.HMAC",
         "grover_weakened", "low", None, ""),

        # --- KDF ---
        ("PY-021", "kdf", "PBKDF2",
         r"hashlib\.pbkdf2_hmac|Crypto\.Protocol\.KDF\.PBKDF2|kdf\.pbkdf2",
         "grover_weakened", "low", "1.2.840.113549.1.5.12", ""),

        ("PY-022", "kdf", "scrypt",
         r"hashlib\.scrypt|Crypto\.Protocol\.KDF\.scrypt",
         "grover_weakened", "low", None, ""),

        ("PY-023", "kdf", "bcrypt",
         r"import\s+bcrypt|bcrypt\.hashpw|bcrypt\.checkpw",
         "grover_weakened", "low", None, ""),

        ("PY-024", "kdf", "Argon2",
         r"from\s+argon2|argon2\.PasswordHasher|argon2\.low_level",
         "grover_weakened", "low", None, ""),

        # --- PQC (liboqs-python) ---
        ("PY-025", "pqc", "ML-KEM (Kyber)",
         r"oqs\.KeyEncapsulation\(\s*['\"]?(Kyber|ML-?KEM)",
         "quantum_safe", "info", None, "liboqs-python"),

        ("PY-026", "pqc", "ML-DSA (Dilithium)",
         r"oqs\.Signature\(\s*['\"]?(Dilithium|ML-?DSA)",
         "quantum_safe", "info", None, "liboqs-python"),

        ("PY-027", "pqc", "SLH-DSA (SPHINCS+)",
         r"oqs\.Signature\(\s*['\"]?SPHINCS",
         "quantum_safe", "info", None, "liboqs-python"),

        ("PY-028", "pqc", "FN-DSA (Falcon)",
         r"oqs\.Signature\(\s*['\"]?Falcon",
         "quantum_safe", "info", None, "liboqs-python"),

        ("PY-029", "pqc", "PQC (generic - verify implementation)",
         r"\b(ML-KEM|ML-DSA|SLH-DSA|FN-DSA|Kyber\d{3,4}|Dilithium\d|SPHINCS\+?)\b",
         "quantum_safe", "info", None,
         "Catch-all safety net: evolving API, configs, comments"),
    ],

    # ========================================================================
    # JAVA
    # ========================================================================
    "java": [
        # --- Symmetric ciphers ---
        ("JAVA-001", "symmetric", "AES",
         r"Cipher\.getInstance\(\s*['\"]AES",
         "grover_weakened", "medium", "2.16.840.1.101.3.4.1", ""),

        ("JAVA-002", "symmetric", "DES / 3DES",
         r"Cipher\.getInstance\(\s*['\"](DESede|DES)\b",
         "already_weak", "critical", None, ""),

        ("JAVA-003", "symmetric", "Blowfish",
         r"Cipher\.getInstance\(\s*['\"]Blowfish",
         "already_weak", "high", None, ""),

        ("JAVA-004", "symmetric", "RC4 / ARCFOUR",
         r"Cipher\.getInstance\(\s*['\"](RC4|ARCFOUR)",
         "already_weak", "critical", None, ""),

        ("JAVA-005", "symmetric", "ChaCha20",
         r"Cipher\.getInstance\(\s*['\"]ChaCha20",
         "grover_weakened", "medium", None, ""),

        # --- Asymmetric ---
        ("JAVA-006", "asymmetric", "RSA",
         r"KeyPairGenerator\.getInstance\(\s*['\"]RSA|Cipher\.getInstance\(\s*['\"]RSA",
         "shor_breakable", "high", "1.2.840.113549.1.1.1", ""),

        ("JAVA-007", "asymmetric", "DSA",
         r"KeyPairGenerator\.getInstance\(\s*['\"]DSA|Signature\.getInstance\(\s*['\"].*withDSA",
         "shor_breakable", "high", "1.2.840.10040.4.1", ""),

        ("JAVA-008", "asymmetric", "EC (ECDSA / ECDH)",
         r"KeyPairGenerator\.getInstance\(\s*['\"]EC\b|Signature\.getInstance\(\s*['\"].*ECDSA|KeyAgreement\.getInstance\(\s*['\"]ECDH",
         "shor_breakable", "high", "1.2.840.10045.2.1", ""),

        ("JAVA-009", "asymmetric", "Ed25519 / X25519",
         r"KeyPairGenerator\.getInstance\(\s*['\"](Ed25519|X25519|EdDSA|XDH)",
         "shor_breakable", "high", None, ""),

        ("JAVA-010", "asymmetric", "Diffie-Hellman",
         r"KeyPairGenerator\.getInstance\(\s*['\"]DH\b|KeyAgreement\.getInstance\(\s*['\"]DH",
         "shor_breakable", "high", "1.2.840.113549.1.3.1", ""),

        # --- Hash ---
        ("JAVA-011", "hash", "MD5",
         r"MessageDigest\.getInstance\(\s*['\"]MD5",
         "already_weak", "critical", "1.2.840.113549.2.5", ""),

        ("JAVA-012", "hash", "SHA-1",
         r"MessageDigest\.getInstance\(\s*['\"]SHA-?1\b",
         "already_weak", "high", "1.3.14.3.2.26", ""),

        ("JAVA-013", "hash", "SHA-2 (224/256/384/512)",
         r"MessageDigest\.getInstance\(\s*['\"]SHA-?(224|256|384|512)\b",
         "grover_weakened", "medium", "2.16.840.1.101.3.4.2", ""),

        ("JAVA-014", "hash", "SHA-3",
         r"MessageDigest\.getInstance\(\s*['\"]SHA3-(224|256|384|512)",
         "grover_weakened", "medium", None, ""),

        # --- MAC ---
        ("JAVA-015", "mac", "HMAC",
         r"Mac\.getInstance\(\s*['\"]Hmac",
         "grover_weakened", "low", None, ""),

        # --- KDF ---
        ("JAVA-016", "kdf", "PBKDF2",
         r"SecretKeyFactory\.getInstance\(\s*['\"]PBKDF2",
         "grover_weakened", "low", "1.2.840.113549.1.5.12", ""),

        ("JAVA-017", "kdf", "BCrypt",
         r"BCryptPasswordEncoder|BCrypt\.(hashpw|checkpw|withDefaults)",
         "grover_weakened", "low", None, "Spring Security / jBCrypt"),

        ("JAVA-018", "kdf", "SCrypt",
         r"SCryptPasswordEncoder|SCryptParametersGenerator",
         "grover_weakened", "low", None, "BouncyCastle / Spring Security"),

        ("JAVA-019", "kdf", "Argon2",
         r"Argon2PasswordEncoder|Argon2Parameters|Argon2BytesGenerator",
         "grover_weakened", "low", None, ""),

        # --- PQC (BouncyCastle) ---
        ("JAVA-020", "pqc", "ML-KEM (Kyber)",
         r"KyberParameterSpec|MLKEMParameterSpec|org\.bouncycastle\.pqc\..*[Kk]yber",
         "quantum_safe", "info", None, "BouncyCastle PQC provider"),

        ("JAVA-021", "pqc", "ML-DSA (Dilithium)",
         r"DilithiumParameterSpec|MLDSAParameterSpec|org\.bouncycastle\.pqc\..*[Dd]ilithium",
         "quantum_safe", "info", None, "BouncyCastle PQC provider"),

        ("JAVA-022", "pqc", "SLH-DSA (SPHINCS+)",
         r"SPHINCSPlusParameterSpec|SLHDSAParameterSpec|org\.bouncycastle\.pqc\..*SPHINCS",
         "quantum_safe", "info", None, "BouncyCastle PQC provider"),

        ("JAVA-023", "pqc", "FN-DSA (Falcon)",
         r"FalconParameterSpec|org\.bouncycastle\.pqc\..*[Ff]alcon",
         "quantum_safe", "info", None, "BouncyCastle PQC provider"),

        ("JAVA-024", "pqc", "PQC (generic - verify implementation)",
         r"\b(ML-KEM|ML-DSA|SLH-DSA|FN-DSA|Kyber\d{3,4}|Dilithium\d|SPHINCS\+?)\b",
         "quantum_safe", "info", None, "Catch-all safety net"),
    ],

    # ========================================================================
    # JAVASCRIPT / NODE
    # ========================================================================
    "javascript": [
        # --- Symmetric ciphers ---
        ("JS-001", "symmetric", "AES",
         r"create(Cipher|Decipher)iv\(\s*['\"]aes-",
         "grover_weakened", "medium", "2.16.840.1.101.3.4.1", "module crypto Node.js"),

        ("JS-002", "symmetric", "AES",
         r"crypto\.subtle\.(encrypt|decrypt|generateKey|importKey)\(\s*\{\s*name:\s*['\"]AES",
         "grover_weakened", "medium", "2.16.840.1.101.3.4.1", "WebCrypto API"),

        ("JS-003", "symmetric", "DES / 3DES",
         r"create(Cipher|Decipher)iv\(\s*['\"]des",
         "already_weak", "critical", None, ""),

        ("JS-004", "symmetric", "RC4",
         r"create(Cipher|Decipher)iv\(\s*['\"]rc4",
         "already_weak", "critical", None, ""),

        ("JS-005", "symmetric", "ChaCha20-Poly1305",
         r"create(Cipher|Decipher)iv\(\s*['\"]chacha20",
         "grover_weakened", "medium", None, ""),

        # --- Asymmetric ---
        ("JS-006", "asymmetric", "RSA",
         r"generateKeyPair(Sync)?\(\s*['\"]rsa|crypto\.subtle\.(generateKey|importKey|sign|encrypt)\(\s*\{\s*name:\s*['\"]RSA",
         "shor_breakable", "high", "1.2.840.113549.1.1.1", ""),

        ("JS-007", "asymmetric", "EC (ECDSA / ECDH)",
         r"generateKeyPair(Sync)?\(\s*['\"]ec\b|name:\s*['\"](ECDSA|ECDH)",
         "shor_breakable", "high", "1.2.840.10045.2.1", ""),

        ("JS-008", "asymmetric", "Ed25519 / X25519",
         r"generateKeyPair(Sync)?\(\s*['\"](ed25519|x25519)|name:\s*['\"](Ed25519|X25519)",
         "shor_breakable", "high", None, ""),

        ("JS-009", "asymmetric", "Diffie-Hellman",
         r"createDiffieHellman\(|generateKeyPair(Sync)?\(\s*['\"]dh\b",
         "shor_breakable", "high", "1.2.840.113549.1.3.1", ""),

        # --- Hash ---
        ("JS-010", "hash", "MD5",
         r"createHash\(\s*['\"]md5",
         "already_weak", "critical", "1.2.840.113549.2.5", ""),

        ("JS-011", "hash", "SHA-1",
         r"createHash\(\s*['\"]sha1|name:\s*['\"]SHA-1",
         "already_weak", "high", "1.3.14.3.2.26", ""),

        ("JS-012", "hash", "SHA-2 (224/256/384/512)",
         r"createHash\(\s*['\"]sha(224|256|384|512)|name:\s*['\"]SHA-(256|384|512)",
         "grover_weakened", "medium", "2.16.840.1.101.3.4.2", ""),

        ("JS-013", "hash", "SHA-3",
         r"createHash\(\s*['\"]sha3-",
         "grover_weakened", "medium", None, ""),

        # --- MAC ---
        ("JS-014", "mac", "HMAC",
         r"createHmac\(|name:\s*['\"]HMAC",
         "grover_weakened", "low", None, ""),

        # --- KDF ---
        ("JS-015", "kdf", "PBKDF2",
         r"crypto\.pbkdf2(Sync)?\(|name:\s*['\"]PBKDF2",
         "grover_weakened", "low", "1.2.840.113549.1.5.12", ""),

        ("JS-016", "kdf", "bcrypt",
         r"require\(\s*['\"]bcrypt|bcrypt\.hash",
         "grover_weakened", "low", None, ""),

        ("JS-017", "kdf", "scrypt",
         r"crypto\.scrypt(Sync)?\(",
         "grover_weakened", "low", None, ""),

        ("JS-018", "kdf", "argon2",
         r"require\(\s*['\"]argon2|argon2\.hash",
         "grover_weakened", "low", None, ""),

        # --- PQC ---
        ("JS-019", "pqc", "ML-KEM (Kyber)",
         r"@noble/post-quantum/ml-kem|pqc-kyber|liboqs-node|ml_?kem|Kyber\d{3,4}",
         "quantum_safe", "info", None, "@noble/post-quantum, liboqs-node, etc."),

        ("JS-020", "pqc", "ML-DSA (Dilithium)",
         r"@noble/post-quantum/ml-dsa|ml_?dsa|Dilithium\d",
         "quantum_safe", "info", None, ""),

        ("JS-021", "pqc", "SLH-DSA (SPHINCS+)",
         r"@noble/post-quantum/slh-dsa|slh_?dsa|SPHINCS\+?",
         "quantum_safe", "info", None, ""),

        ("JS-022", "pqc", "PQC (generic - verify implementation)",
         r"\b(ML-KEM|ML-DSA|SLH-DSA|FN-DSA|Kyber\d{3,4}|Dilithium\d|SPHINCS\+?|Falcon)\b",
         "quantum_safe", "info", None, "Catch-all safety net"),
    ],
}


def _build_patterns():
    """Transform CRYPTO_PATTERNS_RAW (compact tuples) into a list of usable dicts."""
    patterns = []
    for language, entries in CRYPTO_PATTERNS_RAW.items():
        for entry in entries:
            pattern = dict(zip(FIELDS, entry))
            pattern["language"] = language
            patterns.append(pattern)
    return patterns


# Final list used by the scanner: one entry = one detection rule
CRYPTO_PATTERNS = _build_patterns()


def get_patterns_for_language(language: str):
    """Return all rules applicable to a given language."""
    return [p for p in CRYPTO_PATTERNS if p["language"] == language]


def get_patterns_by_category(category: str):
    """Return all rules for a given category (useful for CBOM stats)."""
    return [p for p in CRYPTO_PATTERNS if p["category"] == category]


if __name__ == "__main__":
    print(f"Total rules: {len(CRYPTO_PATTERNS)}")
    print("By language:", dict(Counter(p["language"] for p in CRYPTO_PATTERNS)))
    print("By category:", dict(Counter(p["category"] for p in CRYPTO_PATTERNS)))
    print("By quantum impact:", dict(Counter(p["quantum_impact"] for p in CRYPTO_PATTERNS)))