# Cryptographic Bill of Materials (CBOM) Scanner

CBOM-Scan is a command-line tool that scans Python, Java, and JavaScript source code to inventory cryptographic assets and assess their quantum resilience. It produces a structured CycloneDX CBOM report to help teams identify algorithms at risk and prioritize migration toward post-quantum cryptography (PQC).

## Why this tool

Classical asymmetric algorithms (RSA, ECDSA, Diffie-Hellman) are theoretically breakable by Shor's algorithm on a sufficiently powerful quantum computer. Symmetric algorithms and hash functions are weakened but not broken (Grover's algorithm halves their effective key size). Detecting and cataloguing these assets with a **Cryptographic Bill of Materials** is the first step of any migration toward post-quantum standards (NIST FIPS 203/204/205).

## What it detects

Each finding is classified along three axes:

| Field | Values |
|---|---|
| **Category** | `symmetric`, `asymmetric`, `hash`, `mac`, `kdf`, `pqc` |
| **Quantum impact** | `shor_breakable`, `grover_weakened`, `already_weak`, `quantum_safe` |
| **Risk level** | `critical`, `high`, `medium`, `low`, `info` |

Supported algorithms include AES, DES/3DES, RC4, ChaCha20, RSA, ECDSA/ECDH, Ed25519, X25519, Diffie-Hellman, MD5, SHA-1/2/3, HMAC, PBKDF2, bcrypt, scrypt, Argon2, and post-quantum algorithms (ML-KEM, ML-DSA, SLH-DSA, FN-DSA).

## Features

- Recursive scan of `.py`, `.java`, `.js`, `.jsx`, and `.ts` files
- Regex-based detection rules with OID references where standardized
- Per-finding metadata: file, line, snippet, algorithm, quantum impact, risk level
- CycloneDX JSON report (spec 1.7) with aggregate metrics (by language, category, quantum impact, risk level)
- Post-quantum algorithm detection to surface already-migrated components

## Usage

```bash
python3 main.py <target-directory> --output report.json
```

If `--output` is omitted, the CycloneDX JSON report is printed to standard output.

## Project structure

```
.
├── main.py        # Command-line interface
├── scanner.py     # File traversal and pattern matching
├── patterns.py    # Detection rules (regex, OIDs, metadata)
├── report.py      # JSON report builder
└── sample/
    ├── detected_vulnerabilities/    # Cases the scanner is expected to detect
    └── undetected_patterns/         # Known blind spots (obfuscation, reflection, etc...)
```

## Limitations

- Detection is regex-based and line-oriented, no AST or data-flow analysis.
- Dynamic imports, reflection, and custom cryptographic implementations are likely missed (see `sample/undetected_patterns/`).
- False positives are possible when algorithm names appear in comments or string literals.