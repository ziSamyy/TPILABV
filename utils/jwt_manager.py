from jwt import encode, decode
from datetime import datetime, timedelta, timezone

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    token = encode(to_encode, key='2521104317e46e5b1bd4f67c0f407048bc19877dd5c82e9148604fe3be3b4e2e', algorithm='HS256')
    return token


def validate_token(token: str) -> dict:
    return decode(token, key='2521104317e46e5b1bd4f67c0f407048bc19877dd5c82e9148604fe3be3b4e2e', algorithms=['HS256'])
