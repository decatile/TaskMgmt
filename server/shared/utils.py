from datetime import datetime, UTC
from bcrypt import hashpw, checkpw, gensalt


def hash_password(original: str) -> str:
    return hashpw(original.encode(), gensalt()).decode()


def validate_password(hashed: str, orignal: str) -> bool:
    return checkpw(orignal.encode(), hashed.encode())


def datetime_now() -> datetime:
    return datetime.now(UTC)
