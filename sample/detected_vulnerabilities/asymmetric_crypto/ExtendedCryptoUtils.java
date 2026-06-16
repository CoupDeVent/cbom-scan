package security;

import java.security.*;
import java.security.spec.*;
import javax.crypto.*;
import javax.crypto.spec.*;

/**
 * Extended cryptographic utilities
 * Covers more patterns: DES, 3DES, DH, PBKDF2, BCrypt, Argon2.
 */
public class ExtendedCryptoUtils {

    // --- Vulnerable Symmetric Ciphers ---

    public static byte[] encryptDES(byte[] data, byte[] key, byte[] iv) throws GeneralSecurityException {
        // DES - VULNERABLE! 56-bit key is broken
        Cipher cipher = Cipher.getInstance("DES/CBC/PKCS5Padding");
        DESKeySpec keySpec = new DESKeySpec(key);
        SecretKeyFactory factory = SecretKeyFactory.getInstance("DES");
        SecretKey secretKey = factory.generateSecret(keySpec);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, new IvParameterSpec(iv));
        return cipher.doFinal(data);
    }

    public static byte[] encrypt3DES(byte[] data, byte[] key, byte[] iv) throws GeneralSecurityException {
        // 3DES - Deprecated, vulnerable to Sweet32
        Cipher cipher = Cipher.getInstance("DESede/CBC/PKCS5Padding");
        DESedeKeySpec keySpec = new DESedeKeySpec(key);
        SecretKeyFactory factory = SecretKeyFactory.getInstance("DESede");
        SecretKey secretKey = factory.generateSecret(keySpec);
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, new IvParameterSpec(iv));
        return cipher.doFinal(data);
    }

    // --- Modern Symmetric: AES ---

    public static byte[] encryptAES(byte[] data, byte[] key, byte[] iv) throws GeneralSecurityException {
        // AES - Modern but vulnerable to Grover's algorithm
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        SecretKeySpec keySpec = new SecretKeySpec(key, 0, key.length, "AES");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec, new IvParameterSpec(iv));
        return cipher.doFinal(data);
    }

    public static byte[] encryptAESGCM(byte[] data, byte[] key, byte[] iv) throws GeneralSecurityException {
        // AES-GCM - Authenticated encryption (preferred)
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        SecretKeySpec keySpec = new SecretKeySpec(key, 0, key.length, "AES");
        GCMParameterSpec gcmSpec = new GCMParameterSpec(128, iv);
        cipher.init(Cipher.ENCRYPT_MODE, keySpec, gcmSpec);
        return cipher.doFinal(data);
    }

    // --- Key Generation ---

    public static SecretKey generateAESKey(int keySize) throws NoSuchAlgorithmException {
        KeyGenerator kg = KeyGenerator.getInstance("AES");
        kg.init(keySize);
        return kg.generateKey();
    }

    // --- Asymmetric: RSA ---

    public static KeyPair generateRSAKeyPair(int keySize) throws GeneralSecurityException {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
        kpg.initialize(keySize);
        return kpg.generateKeyPair();
    }

    public static byte[] encryptRSA(byte[] data, PublicKey key) throws GeneralSecurityException {
        Cipher cipher = Cipher.getInstance("RSA/ECB/OAEPWITHSHA256ANDMGF1PADDING");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return cipher.doFinal(data);
    }

    // --- Asymmetric: DSA ---

    public static KeyPair generateDSAKeyPair(int keySize) throws GeneralSecurityException {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("DSA");
        kpg.initialize(keySize);
        return kpg.generateKeyPair();
    }

    public static byte[] signWithDSA(byte[] data, PrivateKey key) throws GeneralSecurityException {
        // DSA - Quantum-vulnerable (Shor's algorithm)
        Signature sig = Signature.getInstance("SHA256withDSA");
        sig.initSign(key);
        sig.update(data);
        return sig.sign();
    }

    // --- Asymmetric: ECC ---

    public static KeyPair generateECKeyPair(String curve) throws GeneralSecurityException {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC");
        kpg.initialize(new ECGenParameterSpec(curve));
        return kpg.generateKeyPair();
    }

    public static KeyPair generateECDSA() throws GeneralSecurityException {
        return generateECKeyPair("secp256r1");
    }

    public static byte[] signWithECDSA(byte[] data, PrivateKey key) throws GeneralSecurityException {
        Signature sig = Signature.getInstance("SHA256withECDSA");
        sig.initSign(key);
        sig.update(data);
        return sig.sign();
    }

    // --- Key Derivation: PBKDF2 ---

    public static byte[] derivePBKDF2(String password, byte[] salt, int iterations, int keyLength)
            throws GeneralSecurityException {
        PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, iterations, keyLength * 8);
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        SecretKey key = factory.generateSecret(spec);
        return key.getEncoded();
    }

    // --- Hash Functions ---

    public static byte[] hashMD5(byte[] data) throws NoSuchAlgorithmException {
        // MD5 - VULNERABLE! Use only for non-cryptographic purposes
        MessageDigest md = MessageDigest.getInstance("MD5");
        return md.digest(data);
    }

    public static byte[] hashSHA1(byte[] data) throws NoSuchAlgorithmException {
        // SHA-1 - Deprecated, collision attacks exist
        MessageDigest md = MessageDigest.getInstance("SHA-1");
        return md.digest(data);
    }

    public static byte[] hashSHA256(byte[] data) throws NoSuchAlgorithmException {
        // SHA-256 - NIST standard, good security
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        return md.digest(data);
    }

    public static byte[] hashSHA512(byte[] data) throws NoSuchAlgorithmException {
        // SHA-512 - Good for long-term security
        MessageDigest md = MessageDigest.getInstance("SHA-512");
        return md.digest(data);
    }

    public static byte[] hashSHA3_256(byte[] data) throws NoSuchAlgorithmException {
        // SHA3-256 - Modern NIST standard
        MessageDigest md = MessageDigest.getInstance("SHA3-256");
        return md.digest(data);
    }

    // --- Diffie-Hellman Key Exchange ---

    public static KeyPair generateDHKeyPair() throws GeneralSecurityException {
        // DH - Quantum-vulnerable, slower than ECDH
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("DH");
        kpg.initialize(2048);
        return kpg.generateKeyPair();
    }

    public static byte[] performDHKeyExchange(PrivateKey privateKey, PublicKey peerPublicKey)
            throws GeneralSecurityException {
        KeyAgreement ka = KeyAgreement.getInstance("DH");
        ka.init(privateKey);
        ka.doPhase(peerPublicKey, true);
        return ka.generateSecret();
    }

    // --- ECDH Key Exchange (preferred over DH) ---

    public static KeyPair generateECDHKeyPair() throws GeneralSecurityException {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC");
        kpg.initialize(new ECGenParameterSpec("secp256r1"));
        return kpg.generateKeyPair();
    }

    public static byte[] performECDHKeyExchange(PrivateKey privateKey, PublicKey peerPublicKey)
            throws GeneralSecurityException {
        KeyAgreement ka = KeyAgreement.getInstance("ECDH");
        ka.init(privateKey);
        ka.doPhase(peerPublicKey, true);
        return ka.generateSecret();
    }

    // --- HMAC ---

    public static byte[] computeHMAC(String algorithm, byte[] key, byte[] message)
            throws GeneralSecurityException {
        Mac mac = Mac.getInstance("Hmac" + algorithm);
        SecretKeySpec keySpec = new SecretKeySpec(key, 0, key.length, "Hmac" + algorithm);
        mac.init(keySpec);
        return mac.doFinal(message);
    }

    public static byte[] computeHMACSHA256(byte[] key, byte[] message) throws GeneralSecurityException {
        return computeHMAC("SHA256", key, message);
    }

    // --- Recommendations ---

    /**
     * Get security recommendations for various use cases.
     */
    public static String getSecurityRecommendations() {
        return "Symmetric: Use AES-GCM (256-bit key)\n" +
               "Signing: Use ECDSA with NIST curves or EdDSA\n" +
               "Key Exchange: Use ECDH or X25519\n" +
               "Hashing: Use SHA-256 or SHA-512 (never MD5/SHA1)\n" +
               "Password Hashing: Use bcrypt, scrypt, or Argon2\n" +
               "Key Derivation: Use PBKDF2 with 100k+ iterations\n" +
               "Quantum Ready: Plan migration to ML-KEM and ML-DSA";
    }
}
