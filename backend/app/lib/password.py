# app/security.py
from __future__ import annotations
import hmac
import os
from hashlib import sha256
from passlib.context import CryptContext
from app.settings import settings


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    # You can tune these based on your server capacity:
    # "argon2__time_cost": 3,
    # "argon2__memory_cost": 102400,  # ~100 MB
    # "argon2__parallelism": 8,
)

# If you must use bcrypt (fallback):
# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto",
#     bcrypt__rounds=12,  # 12–14 typical; raise if CPU allows
# )

# ---- Optional peppering (recommended) ----
# Keep this in env/secret manager. Rotate very rarely and plan a rehash migration.
PEPPER = settings.PASSWORD_HASH_SECRET_KEY  # e.g., a 32+ random bytes base64 string

def _pepper(password: str) -> bytes:
    if not PEPPER:
        # No pepper configured; return raw UTF-8 bytes
        return password.encode("utf-8")
    # HMAC-SHA256 with a secret pepper; constant-time and deterministic
    return hmac.new(PEPPER.encode("utf-8"), password.encode("utf-8"), sha256).digest()

def hash_password(raw_password: str) -> str:
    """
    Hash a raw password. Handles peppering and returns an encoded hash string.
    """
    return pwd_context.hash(_pepper(raw_password))

def verify_password(raw_password: str, stored_hash: str) -> bool:
    """
    Constant-time verification. DO NOT pre-hash or modify `stored_hash`.
    """
    return pwd_context.verify(_pepper(raw_password), stored_hash)

def needs_rehash(stored_hash: str) -> bool:
    """
    If policy parameters changed (e.g., higher cost), this will return True.
    Rehash on next successful login.
    """
    return pwd_context.needs_update(stored_hash)
