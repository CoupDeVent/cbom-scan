/**
 * JavaScript/Node.js cryptographic examples
 * Covers AES, RSA, hashing, PBKDF2, scrypt, and key exchange patterns.
 */

const crypto = require('crypto');

// --- Symmetric Encryption: Vulnerable Ciphers ---

function encryptDES(data, key, iv) {
  // DES - VULNERABLE! 56-bit key is broken
  const cipher = crypto.createCipheriv('des-cbc', key, iv);
  return Buffer.concat([cipher.update(data), cipher.final()]);
}

function encryptRC4(data, key) {
  // RC4 - BROKEN stream cipher, do not use
  const cipher = crypto.createCipheriv('rc4', key, '');
  return Buffer.concat([cipher.update(data), cipher.final()]);
}

// --- Symmetric Encryption: Modern (vulnerable to Grover's) ---

function encryptAES256CBC(data, key, iv) {
  // AES-256-CBC - Good but not authenticated
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  return Buffer.concat([cipher.update(data), cipher.final()]);
}

function encryptAES256GCM(data, key, iv, aad) {
  // AES-256-GCM - Authenticated encryption (recommended)
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  if (aad) cipher.setAAD(aad);
  const encrypted = Buffer.concat([cipher.update(data), cipher.final()]);
  const authTag = cipher.getAuthTag();
  return { encrypted, authTag };
}

function encryptChaCha20(data, key, nonce) {
  // ChaCha20-Poly1305 - Modern stream cipher
  const cipher = crypto.createCipheriv('chacha20-poly1305', key, nonce);
  const encrypted = Buffer.concat([cipher.update(data), cipher.final()]);
  const authTag = cipher.getAuthTag();
  return { encrypted, authTag };
}

// --- Asymmetric: RSA ---

function generateRSAKeyPair(bits = 2048) {
  // RSA - Quantum-vulnerable (Shor's algorithm)
  const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: bits,
    publicKeyEncoding: {
      type: 'spki',
      format: 'pem'
    },
    privateKeyEncoding: {
      type: 'pkcs8',
      format: 'pem'
    }
  });
  return { publicKey, privateKey };
}

function encryptRSA(data, publicKeyPem) {
  // RSA-OAEP encryption
  return crypto.publicEncrypt(
    {
      key: publicKeyPem,
      padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      oaepHash: 'sha256'
    },
    data
  );
}

function signRSA(data, privateKeyPem) {
  // RSA-PSS signature (better than PKCS#1 v1.5)
  const sign = crypto.createSign('RSA-SHA256');
  sign.update(data);
  return sign.sign({
    key: privateKeyPem,
    padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
    saltLength: 32
  });
}

// --- Asymmetric: ECDSA ---

function generateECKeyPair(namedCurve = 'prime256v1') {
  // ECC (ECDSA) - Quantum-vulnerable but more efficient than RSA
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ec', {
    namedCurve: namedCurve,
    publicKeyEncoding: {
      type: 'spki',
      format: 'pem'
    },
    privateKeyEncoding: {
      type: 'pkcs8',
      format: 'pem'
    }
  });
  return { publicKey, privateKey };
}

function signECDSA(data, privateKeyPem) {
  // ECDSA signature
  const sign = crypto.createSign('SHA256');
  sign.update(data);
  return sign.sign(privateKeyPem);
}

function verifyECDSA(data, signature, publicKeyPem) {
  const verify = crypto.createVerify('SHA256');
  verify.update(data);
  return verify.verify(publicKeyPem, signature);
}

// --- Asymmetric: Ed25519 (Post-quantum safe for signatures) ---

function generateEd25519KeyPair() {
  // Ed25519 - Post-quantum safe for signatures
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519', {
    publicKeyEncoding: {
      type: 'spki',
      format: 'pem'
    },
    privateKeyEncoding: {
      type: 'pkcs8',
      format: 'pem'
    }
  });
  return { publicKey, privateKey };
}

function signEd25519(data, privateKeyPem) {
  return crypto.sign(null, data, privateKeyPem);
}

function verifyEd25519(data, signature, publicKeyPem) {
  return crypto.verify(null, data, publicKeyPem, signature);
}

// --- Key Exchange: ECDH ---

function generateECDHKeyPair(namedCurve = 'prime256v1') {
  // ECDH - Quantum-vulnerable but preferred over DH
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ec', {
    namedCurve: namedCurve
  });
  return { publicKey, privateKey };
}

function computeECDHSecret(privateKey, publicKeyPem) {
  // Compute shared secret via ECDH
  const ecdh = crypto.createECDH(privateKey.asymmetricKeyDetails.namedCurve);
  ecdh.setPrivateKey(privateKey.export({ format: 'der', type: 'pkcs8' }));
  const publicKey = crypto.createPublicKey(publicKeyPem);
  return ecdh.computeSecret(publicKey.export({ format: 'der', type: 'spki' }));
}

// --- Diffie-Hellman (quantum-vulnerable, slower than ECDH) ---

function generateDHKeyPair() {
  // DH - Slower and less secure than ECDH
  const dh = crypto.createDiffieHellman(2048);
  const publicKey = dh.generateKeys();
  return { dh, publicKey };
}

// --- Hashing ---

function hashMD5(data) {
  // MD5 - VULNERABLE! Collision attacks are practical
  return crypto.createHash('md5').update(data).digest('hex');
}

function hashSHA1(data) {
  // SHA-1 - Deprecated, collision attacks exist
  return crypto.createHash('sha1').update(data).digest('hex');
}

function hashSHA256(data) {
  // SHA-256 - NIST standard, secure
  return crypto.createHash('sha256').update(data).digest('hex');
}

function hashSHA512(data) {
  // SHA-512 - Good for long-term security
  return crypto.createHash('sha512').update(data).digest('hex');
}

function hashSHA3_256(data) {
  // SHA3-256 - Modern NIST standard
  return crypto.createHash('sha3-256').update(data).digest('hex');
}

function hashBLAKE2b512(data) {
  // BLAKE2b - Fast and secure
  return crypto.createHash('blake2b512').update(data).digest('hex');
}

// --- Key Derivation Functions ---

function derivePBKDF2(password, salt, iterations = 100000, keyLength = 32) {
  // PBKDF2 - Good for password hashing
  return crypto.pbkdf2Sync(password, salt, iterations, keyLength, 'sha256').toString('hex');
}

function deriveScrypt(password, salt, keyLength = 32) {
  // scrypt - Better security properties than PBKDF2
  return crypto.scryptSync(password, salt, keyLength).toString('hex');
}

// --- HMAC ---

function computeHMACSHA256(key, message) {
  // HMAC-SHA256 for message authentication
  return crypto.createHmac('sha256', key).update(message).digest('hex');
}

function verifyHMACSHA256(key, message, signature) {
  // Verify HMAC with constant-time comparison
  const expected = computeHMACSHA256(key, message);
  return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
}

// --- Random Generation ---

function generateRandomBytes(length = 32) {
  return crypto.randomBytes(length).toString('hex');
}

// --- WebCrypto API (Browser compatibility) ---

async function generateWebCryptoAESKey(keySize = 256) {
  // Using Web Crypto API
  if (typeof globalThis.crypto === 'undefined') return null;
  const key = await globalThis.crypto.subtle.generateKey(
    { name: 'AES-GCM', length: keySize },
    true,
    ['encrypt', 'decrypt']
  );
  return key;
}

// --- Recommendations ---

function getRecommendations() {
  return {
    symmetric: 'Use AES-256-GCM (authenticated encryption)',
    hashing: 'Use SHA-256 or SHA-512 (never MD5/SHA1)',
    signing: 'Use Ed25519 (post-quantum safe) or ECDSA',
    keyExchange: 'Use ECDH (P-256) or X25519',
    keyDerivation: 'Use scrypt or PBKDF2 with 100k+ iterations',
    random: 'Always use crypto.randomBytes()',
    quantum: 'Transition to liboqs-node or wait for native ML-KEM/ML-DSA support'
  };
}

module.exports = {
  // Encryption
  encryptDES,
  encryptRC4,
  encryptAES256CBC,
  encryptAES256GCM,
  encryptChaCha20,
  
  // RSA
  generateRSAKeyPair,
  encryptRSA,
  signRSA,
  
  // ECC
  generateECKeyPair,
  signECDSA,
  verifyECDSA,
  
  // Ed25519
  generateEd25519KeyPair,
  signEd25519,
  verifyEd25519,
  
  // Key Exchange
  generateECDHKeyPair,
  computeECDHSecret,
  generateDHKeyPair,
  
  // Hashing
  hashMD5,
  hashSHA1,
  hashSHA256,
  hashSHA512,
  hashSHA3_256,
  hashBLAKE2b512,
  
  // KDF
  derivePBKDF2,
  deriveScrypt,
  
  // HMAC
  computeHMACSHA256,
  verifyHMACSHA256,
  
  // Random
  generateRandomBytes,
  
  // Web Crypto
  generateWebCryptoAESKey,
  
  // Info
  getRecommendations
};
