from estatejet.config import PasswordContext


def get_password_hash(password: str):
    """
    Hashes Password
    Args:
        password:

    Returns:

    """
    return PasswordContext.hash(password)