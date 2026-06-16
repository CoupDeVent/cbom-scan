"""
ustom homemade cipher implementation
WARNING: Scanner will NOT detect this as it doesn't use recognized crypto libraries.
This demonstrates why homemade crypto should never be used.
"""

class SimpleCipher:
    """Homemade cipher - DO NOT USE IN PRODUCTION!"""
    
    def __init__(self, key: str):
        self.key = key
    
    def encrypt(self, plaintext: str) -> str:
        """Simple XOR cipher - breaks immediately with frequency analysis."""
        result = []
        key_index = 0
        for char in plaintext:
            key_char = self.key[key_index % len(self.key)]
            encrypted_char = chr(ord(char) ^ ord(key_char))
            result.append(encrypted_char)
            key_index += 1
        return ''.join(result)
    
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt using XOR (symmetric)."""
        return self.encrypt(ciphertext)


class HomemadeAES:
    """Fake AES implementation - completely insecure."""
    
    def __init__(self, key: bytes):
        self.key = key
        self.state = [[0] * 4 for _ in range(4)]
    
    def substitute_bytes(self):
        """Attempt at S-box substitution - not cryptographically sound."""
        for row in self.state:
            for i in range(len(row)):
                row[i] = (row[i] + 1) % 256
    
    def encrypt_block(self, plaintext: bytes) -> bytes:
        """Homemade block cipher - extremely weak."""
        result = bytearray(plaintext)
        for i in range(10):  # Fake rounds
            for j in range(len(result)):
                result[j] ^= self.key[j % len(self.key)]
                result[j] = (result[j] + i) % 256
        return bytes(result)


class WeakKDF:
    """Custom key derivation - NOT recommended."""
    
    @staticmethod
    def derive_key(password: str, salt: str, iterations: int = 1) -> str:
        """Weak key derivation - only one iteration of hashing."""
        result = password + salt
        for _ in range(iterations):
            result = str(hash(result))  # Python's hash is not cryptographic!
        return result


def custom_hash(data: str) -> str:
    """Homemade hash function - completely broken."""
    result = 0
    for char in data:
        result = ((result << 5) + result) ^ ord(char)  # Simple mixing
    return hex(result)


def roll_cipher(text: str, shift: int) -> str:
    """Caesar cipher - 1500 years old, trivial to break."""
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result.append(chr(base + shifted))
        else:
            result.append(char)
    return ''.join(result)


# --- Usage examples (NOT for production) ---

if __name__ == '__main__':
    # Simple XOR cipher
    cipher = SimpleCipher('secret_key')
    encrypted = cipher.encrypt('Hello World')
    print(f'Encrypted: {encrypted}')
    
    # Homemade AES
    fake_aes = HomemadeAES(b'16bytes_key_____')
    ciphertext = fake_aes.encrypt_block(b'0123456789ABCDEF')
    print(f'Fake AES result: {ciphertext}')
    
    # Weak KDF
    key = WeakKDF.derive_key('password', 'salt_value', iterations=1)
    print(f'Derived key: {key}')
    
    # Caesar cipher
    text = 'Secret Message'
    shifted = roll_cipher(text, 3)
    print(f'Caesar cipher: {shifted}')
