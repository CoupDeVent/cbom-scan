package security;

import java.security.*;
import java.security.spec.ECGenParameterSpec;
import javax.crypto.*;

/**
 * Java cryptographic utilities
 * EC key generation, ECDSA signing, and hashing.
 */
public class CryptoUtils {

    // --- EC key generation ---

    public static KeyPair generateECKeyPair() throws GeneralSecurityException {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC");
        kpg.initialize(new ECGenParameterSpec("secp256r1"));
        return kpg.generateKeyPair();
    }

    public static KeyPair generateRSAKeyPair() throws GeneralSecurityException {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
        kpg.initialize(4096);
        return kpg.generateKeyPair();
    }

    // --- Signature ---

    public static byte[] signWithECDSA(byte[] data, PrivateKey key) throws GeneralSecurityException {
        Signature sig = Signature.getInstance("SHA256withECDSA");
        sig.initSign(key);
        sig.update(data);
        return sig.sign();
    }

    public static byte[] signLegacy(byte[] data, PrivateKey key) throws GeneralSecurityException {
        Signature sig = Signature.getInstance("SHA1withRSAEncryption");  // SHA-1 deprecated!
        sig.initSign(key);
        sig.update(data);
        return sig.sign();
    }

    // --- Hashing ---

    public static byte[] hashData(byte[] data) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        return md.digest(data);
    }

    public static byte[] hashLegacy(byte[] data) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("SHA-1");  // deprecated
        return md.digest(data);
    }

    // --- AES encryption ---

    public static SecretKey generateAESKey() throws NoSuchAlgorithmException {
        KeyGenerator kg = KeyGenerator.getInstance("AES");
        kg.init(256);
        return kg.generateKey();
    }

    public static byte[] encryptAES(byte[] data, SecretKey key) throws GeneralSecurityException {
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return cipher.doFinal(data);
    }
}
