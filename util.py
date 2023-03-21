import hashlib
import secrets


def hash_password(password: str, password_salt: str) -> str:
    """Hashes a password with a salt using SHA-256.

    :param password: password to hash
    :param password_salt: salt to append

    :returns: password hashed using SHA-256"""
    return hashlib.sha256((password + password_salt).encode()).hexdigest()


def verify_password(password: str, password_hash: str, password_salt: str) -> bool:
    """Checks if hashes of a password and a salt match a given hash.

    :param password: password to verify
    :param password_hash: hash of the original password
    :param password_salt: salt used to hash the original password

    :returns: True if computed hashes match, False if not"""
    return hash_password(password, password_salt) == password_hash


def generate_salt() -> str:
    """Generates a random string of 16 hex characters.

    :returns: random salt"""
    return secrets.token_hex(16)


def generate_password_hash(password: str) -> (str, str):
    """Generates a random salt and hashes a password with it.

    :param password: password to hash

    :returns: password hashed using SHA-256 and newly generated salt"""
    password_salt = generate_salt()
    password_hash = hash_password(password, password_salt)
    return password_hash, password_salt
