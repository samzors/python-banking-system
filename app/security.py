import hashlib
import secrets


def hash_pin(pin: str) -> str:
    """
    Securely hash a PIN using PBKDF2-HMAC-SHA256.

    A random salt is generated for every PIN.
    """

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode("utf-8"),
        salt,
        100_000
    )

    return f"{salt.hex()}:{password_hash.hex()}"


def verify_pin(pin: str, stored_hash: str) -> bool:
    """Verify a PIN against its stored hash."""

    try:
        salt_hex, hash_hex = stored_hash.split(":")

        salt = bytes.fromhex(salt_hex)
        stored_password_hash = bytes.fromhex(hash_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            pin.encode("utf-8"),
            salt,
            100_000
        )

        return secrets.compare_digest(
            password_hash,
            stored_password_hash
        )

    except (ValueError, TypeError):
        return False