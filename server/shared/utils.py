from datetime import UTC, datetime
import bcrypt


def hash_password(original: str) -> str:
    return bcrypt.hashpw(original.encode(), bcrypt.gensalt()).decode()


def validate_password(hashed: str, original: str) -> bool:
    return bcrypt.checkpw(original.encode(), hashed.encode())


def utc_now() -> datetime:
    return datetime.now(UTC)
