from coolname import generate_slug
import secrets


def generate_username() -> str:
    return f"{generate_slug(2)}-{secrets.randbelow(10000):04d}"  # brave-tiger-0742
