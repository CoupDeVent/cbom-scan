"""
Cryptographic calls hidden from simple regex patterns
WARNING: Scanner will NOT detect these patterns as they don't match the regex rules.
This shows the limitations of pattern-based detection.
"""

import importlib
import sys

# --- String-based imports (won't match simple regex) ---

def dynamic_crypto_import():
    """Import crypto library using string manipulation."""
    lib_name = 'Crypto' + '.Cipher'
    crypto_lib = importlib.import_module(lib_name)
    return crypto_lib


def get_cipher_class():
    """Get AES class through indirect method."""
    cipher_module_name = 'Crypto.Cipher'
    cipher_class_name = 'AES'
    module = __import__(cipher_module_name, fromlist=[cipher_class_name])
    return getattr(module, cipher_class_name)


# --- Dynamic function calls (won't match regex) ---

def encrypt_data(data, key, iv):
    """Uses dynamically constructed function name."""
    cipher_class = get_cipher_class()
    # Function name built at runtime
    mode = 'MODE_CBC'
    cipher = cipher_class.new(key, getattr(cipher_class, mode), iv)
    return cipher.encrypt(data)


def hash_password(password):
    """Hash using dynamically selected algorithm."""
    hash_algorithms = {
        'weak': 'MD5',
        'better': 'SHA256',
        'best': 'SHA512'
    }
    
    # String-based algorithm selection won't be detected
    algo = 'weak'  # This could be 'MD5' or other vulnerable option
    full_module_name = 'hashlib'
    hashlib_module = __import__(full_module_name)
    
    # getattr with string - won't match simple regex
    hash_func = getattr(hashlib_module, hash_algorithms[algo].lower())
    return hash_func(password.encode()).hexdigest()


# --- Crypto calls hidden in list comprehensions ---

def batch_encrypt(data_list, key, iv):
    """Encrypt multiple items using list comprehension."""
    cipher_class = get_cipher_class()
    # This pattern won't be detected by simple regex
    encrypted = [
        cipher_class.new(key, getattr(cipher_class, 'MODE_CBC'), iv).encrypt(item)
        for item in data_list
    ]
    return encrypted


# --- RSA via indirect method ---

def generate_rsa_key():
    """Generate RSA key through indirect access."""
    # Method 1: String-based import
    module_name = 'Crypto.PublicKey'
    class_name = 'RSA'
    module = importlib.import_module(module_name)
    rsa_class = getattr(module, class_name)
    
    # Method 2: String-based method call
    method_name = 'generate'
    generate_method = getattr(rsa_class, method_name)
    return generate_method(2048)


# --- Cryptographic operations in loops (harder to detect) ---

def multi_pass_encryption(data, key):
    """Apply encryption multiple times through loop."""
    result = data
    for i in range(3):
        cipher_module = dynamic_crypto_import()
        # Dynamic module access makes regex harder
        cipher = cipher_module.AES.new(key, cipher_module.AES.MODE_ECB)
        result = cipher.encrypt(result)
    return result


# --- Environment variable-based crypto ---

import os

def get_encryption_key_from_env():
    """Encryption key built from environment at runtime."""
    env_vars = ['CRYPTO_KEY_' + str(i) for i in range(4)]
    key_parts = [os.environ.get(var, '') for var in env_vars]
    # Scanner won't detect this as CRYPTO_KEY usage
    return ''.join(key_parts)


def encrypt_with_runtime_key(data):
    """Use environment-sourced key."""
    key = get_encryption_key_from_env()
    cipher_class = get_cipher_class()
    cipher = cipher_class.new(key.encode()[:32], cipher_class.MODE_ECB)
    return cipher.encrypt(data)


# --- Via configuration files (not in code) ---

def load_crypto_from_config():
    """Load cryptographic algorithm from external config."""
    # This won't be detected as it's loaded from file, not hardcoded
    import json
    config = {
        'algorithm': 'AES',  # Could be MD5, RC4, etc.
        'mode': 'MODE_CBC',
        'key_size': 256
    }
    return config


# --- Obfuscated function names ---

def _x(d, k, i):
    """Function with obscured name using crypto."""
    c = get_cipher_class()
    return c.new(k, getattr(c, 'MODE_CBC'), i).encrypt(d)


def __xor__(a, b):
    """Operator overloading with cryptographic operation."""
    # This pattern might not be recognized
    return bytes(x ^ y for x, y in zip(a, b))


# --- Crypto in lambda functions ---

encrypt_lambda = lambda data, key, iv: get_cipher_class().new(key, getattr(get_cipher_class(), 'MODE_CBC'), iv).encrypt(data)

hash_lambda = lambda x: __import__('hashlib').md5(x.encode()).hexdigest()


# --- Examples of what won't be detected ---

class EncryptionWrapper:
    """Wrapper that hides direct crypto calls."""
    
    def __init__(self, key):
        self.key = key
        # Dynamic module loading
        self._cipher_module = importlib.import_module('Crypto.Cipher')
    
    def _process(self, data, iv, operation='encrypt'):
        """Internal method with dynamic operation."""
        cipher = self._cipher_module.AES.new(self.key, self._cipher_module.AES.MODE_CBC, iv)
        return getattr(cipher, operation)(data)
    
    def process(self, data, iv):
        """Public API that hides crypto call."""
        return self._process(data, iv)


# --- Factory pattern hiding crypto ---

class CipherFactory:
    """Factory that creates ciphers without obvious crypto imports."""
    
    @staticmethod
    def create_cipher(algo_name, key, mode_name):
        """Factory method for creating ciphers."""
        # This indirection makes detection harder
        crypto = importlib.import_module('Crypto.Cipher')
        algo_class = getattr(crypto, algo_name)
        mode = getattr(algo_class, 'MODE_' + mode_name)
        return algo_class.new(key, mode)

