from cryptography.fernet import Fernet
import os

def encrypt(data: str) -> str:
    """Encrypt data - تشفير البيانات"""
    key = os.getenv('ENCRYPTION_KEY', 'default-key-32-chars-exactly').encode()[:32]
    # Pad or truncate to 32 bytes
    key = key.ljust(32, b'=')[:32]
    
    # Create a valid Fernet key from our 32-byte key
    import base64
    fernet_key = base64.urlsafe_b64encode(key)
    
    cipher = Fernet(fernet_key)
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()

def decrypt(encrypted_data: str) -> str:
    """Decrypt data - فك تشفير البيانات"""
    key = os.getenv('ENCRYPTION_KEY', 'default-key-32-chars-exactly').encode()[:32]
    key = key.ljust(32, b'=')[:32]
    
    import base64
    fernet_key = base64.urlsafe_b64encode(key)
    
    cipher = Fernet(fernet_key)
    decrypted = cipher.decrypt(encrypted_data.encode())
    return decrypted.decode()
