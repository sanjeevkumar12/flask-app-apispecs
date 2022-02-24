from cryptography.fernet import Fernet


def generate_key() -> str:
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    return key.decode()


def encrypt_message(message: str, key: str) -> str:
    """
    Encrypts a message
    """

    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    return encrypted_message.decode()


def decrypt_message(encrypted_message: str, key: str) -> str:
    """
    Encrypts a message
    """

    encoded_message = encrypted_message.encode()
    f = Fernet(key)
    encrypted_message = f.decrypt(encoded_message)

    return encrypted_message.decode()
