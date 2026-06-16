"""
deprecated_apis.java - Deprecated cryptographic APIs and old libraries
WARNING: Scanner may not detect these if using old/custom library versions.
"""

import java.security.*;
import javax.crypto.*;
import java.util.Date;

/**
 * Examples of outdated cryptographic patterns that won't be detected
 * if using non-standard library versions or obsolete APIs.
 */

public class DeprecatedCryptoAPIs {

    // --- Deprecated Cipher Specifications (SunJSSE older versions) ---

    public static byte[] encryptWithWeakSSL(String data, byte[] key) throws Exception {
        // SSLContext with deprecated protocol versions
        SSLContext sslContext = SSLContext.getInstance("SSLv3");  // DEPRECATED!
        // Old versions of JDK may not report this as problematic
        return data.getBytes();
    }

    public static byte[] encryptWithOldTLS(String data) throws Exception {
        // TLS 1.0 / 1.1 are deprecated
        SSLContext sslContext = SSLContext.getInstance("TLSv1");  // DEPRECATED!
        return data.getBytes();
    }

    // --- Custom message digest implementations that won't be caught ---

    private static class CustomMessageDigest {
        """
        Homemade hash implementation that won't match standard library patterns.
        """
        
        public static byte[] hash(byte[] data) {
            // Custom hashing logic that doesn't use MessageDigest.getInstance()
            byte[] result = new byte[data.length];
            for (int i = 0; i < data.length; i++) {
                result[i] = (byte) ((data[i] + i) & 0xFF);
            }
            return result;
        }
    }

    // --- Reflection-based crypto (won't be detected) ---

    public static Object getHashAlgorithm(String algoName) throws Exception {
        // Using reflection to get cipher - won't match direct pattern
        String className = "java.security.MessageDigest";
        Class<?> clazz = Class.forName(className);
        Method method = clazz.getMethod("getInstance", String.class);
        return method.invoke(null, algoName);
    }

    // --- Provider-specific algorithms (may not be detected) ---

    public static void encryptWithProviderAlgo() throws Exception {
        // Using provider-specific algorithm names
        String[] algorithms = {
            "RSA/ECB/NoPadding",  // Provider-specific
            "DES/ECB/PKCS5Padding",  // Old cipher
        };
        
        for (String algo : algorithms) {
            try {
                Cipher cipher = Cipher.getInstance(algo);
                // This might not be detected if running on specific provider
            } catch (NoSuchAlgorithmException e) {
                // Silent failure - algorithm not available
            }
        }
    }

    // --- Hardcoded algorithm strings (won't be detected) ---

    private static final String WEAK_ALGO = "MD5";  // Hardcoded weak algorithm
    private static final String OLD_CIPHER = "DES";  // Hardcoded old cipher
    private static final String DEPRECATED_HASH = "SHA-1";  // Deprecated

    public static byte[] hashWithStringAlgo(String algoName, byte[] data) throws Exception {
        // Using string variable instead of literal - may evade detection
        MessageDigest md = MessageDigest.getInstance(algoName);
        return md.digest(data);
    }

    // --- Conditional crypto (harder to detect statically) ---

    public static byte[] selectiveEncryption(byte[] data, boolean useWeak) throws Exception {
        String algorithm = useWeak ? "DES" : "AES";
        Cipher cipher = Cipher.getInstance(algorithm + "/ECB/PKCS5Padding");
        
        // If useWeak=true, DES is used but might not be detected by simple scan
        return data;
    }

    // --- Legacy bouncycastle usage ---

    public static void oldBouncyCastleExample() throws Exception {
        /*
         * If using BouncyCastle < 1.60, these might not be detected:
         * - org.bouncycastle.crypto.engines.DESedeEngine
         * - org.bouncycastle.crypto.modes.ECBBlockCipher
         * 
         * Modern versions have different class names
         */
    }

    // --- Jython/IronPython/Groovy crypto (not pure Java) ---

    public static void externalLanguageCrypto() {
        // Crypto called from other JVM languages won't be detected by Java scanner
        // Example: Groovy code
        String groovyCode = """
            def cipher = 'DES'.encodeAsBase64()  // Groovy extension
            def result = doEncryption(cipher)
        """;
    }

    // --- Dynamically loaded crypto libraries ---

    public static byte[] encryptWithDynamicLib(byte[] data) throws Exception {
        // Loading library name from configuration/database
        String libClass = System.getProperty("crypto.library", "javax.crypto.Cipher");
        Class<?> dynamicClass = Class.forName(libClass);
        
        // This won't be detected as it's resolved at runtime
        return data;
    }

    // --- Cipher service providers (dynamic lookup) ---

    public static void dynamicProvider() throws Exception {
        String providerName = "SunJSSE";  // Or custom provider
        Provider provider = Security.getProvider(providerName);
        
        if (provider != null) {
            // Getting cipher through provider lookup won't be directly detected
            for (String algorithm : new String[]{"DES", "MD5", "SHA-1"}) {
                Object service = provider.get("MessageDigest." + algorithm);
                // This dynamic lookup may not trigger detection
            }
        }
    }

    // --- Comments that reference crypto but don't use it directly ---

    private static byte[] legacyEncryption(byte[] data) {
        // This function used to use DES but was refactored
        // The comment still mentions DES - old habit
        // Original code: Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        return data;
    }

    // --- Masked algorithm names ---

    private static String getAlgorithm() {
        String base = "SHA";
        String version = "-1";  // This evaluates to "SHA-1" at runtime
        return base + version;
    }

    public static byte[] hashWithMaskedName(byte[] data) throws Exception {
        String algo = getAlgorithm();  // Returns "SHA-1" but not directly visible
        MessageDigest md = MessageDigest.getInstance(algo);
        return md.digest(data);
    }

    // --- Mixins and composition (won't be detected) ---

    public interface CryptoProvider {
        byte[] encrypt(byte[] data, byte[] key);
    }

    private static class WeakCryptoImpl implements CryptoProvider {
        // Implementation might be instantiated dynamically
        public byte[] encrypt(byte[] data, byte[] key) {
            // Weak crypto hidden in interface implementation
            return data;
        }
    }

    // --- Native crypto calls (won't be detected by Java scanner) ---

    public static class NativeCrypto {
        static {
            // Load native library at runtime
            // System.loadLibrary("crypto_native");
        }

        // Crypto operations delegated to native C/C++ code
        public native byte[] encryptNative(byte[] data, byte[] key);
    }

    // --- RECOMMENDATIONS ---

    /**
     * What should be upgraded:
     * - Replace SSLv3, TLSv1.0, TLSv1.1 with TLS 1.2+
     * - Replace MD5, SHA-1 with SHA-256+
     * - Replace DES, 3DES with AES
     * - Replace RSA with 2048+ bit keys
     * - Replace custom crypto with standard libraries
     * - Avoid reflection-based crypto lookup
     * - Use secure defaults, not conditional weak crypto
     */
    
    public static String getUpgradeGuide() {
        return "Use modern Java Cryptography Architecture (JCA) with:" +
               "\n  - Ciphers: AES-256-GCM" +
               "\n  - Hashing: SHA-256, SHA-512, SHA-3" +
               "\n  - KDF: PBKDF2, bcrypt, scrypt, Argon2" +
               "\n  - Asymmetric: RSA 2048+, ECDSA, EdDSA" +
               "\n  - TLS: TLS 1.3+";
    }
}
