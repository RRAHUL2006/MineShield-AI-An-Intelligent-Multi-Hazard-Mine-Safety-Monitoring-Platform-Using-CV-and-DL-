"""
security.py

JWT Authentication Utilities
"""

from datetime import datetime, timedelta

from jose import jwt, JWTError

from passlib.context import CryptContext

# ==========================================================
# Configuration
# ==========================================================

SECRET_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12   # 12 Hours

# ==========================================================
# Password Hashing
# ==========================================================

pwd_context = CryptContext(

    schemes=["bcrypt"],

    deprecated="auto"

)

# ==========================================================
# Hash Password
# ==========================================================

def hash_password(password: str):

    return pwd_context.hash(password)

# ==========================================================
# Verify Password
# ==========================================================

def verify_password(

    plain_password,

    hashed_password

):

    return pwd_context.verify(

        plain_password,

        hashed_password

    )

# ==========================================================
# Create JWT Token
# ==========================================================

def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(

        minutes=ACCESS_TOKEN_EXPIRE_MINUTES

    )

    payload.update({

        "exp": expire

    })

    return jwt.encode(

        payload,

        SECRET_KEY,

        algorithm=ALGORITHM

    )

# ==========================================================
# Decode JWT
# ==========================================================

def decode_token(token: str):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]

        )

        return payload

    except JWTError:

        return None