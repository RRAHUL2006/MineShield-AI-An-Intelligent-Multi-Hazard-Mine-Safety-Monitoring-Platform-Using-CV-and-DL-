"""
auth.py

JWT Authentication Logic
"""

from datetime import datetime

from fastapi import Depends, HTTPException

from fastapi.security import OAuth2PasswordBearer

from backend.security import (

    verify_password,

    create_access_token,

    decode_token

)

from backend.users import (

    get_user,

    set_last_login

)

# ==========================================================
# OAuth2
# ==========================================================

oauth2_scheme = OAuth2PasswordBearer(

    tokenUrl="/login"

)

# ==========================================================
# Authenticate User
# ==========================================================

def authenticate_user(

    username: str,

    password: str

):

    user = get_user(username)

    if user is None:

        return None

    if not user["active"]:

        raise HTTPException(

            status_code=403,

            detail="User account is disabled."

        )

    if not verify_password(

        password,

        user["password"]

    ):

        return None

    # ----------------------------------------

    set_last_login(

        username,

        datetime.now().strftime(

            "%d-%m-%Y %H:%M:%S"

        )

    )

    # ----------------------------------------

    token = create_access_token(

        {

            "sub": user["username"],

            "role": user["role"]

        }

    )

    return {

        "access_token": token,

        "token_type": "bearer",

        "username": user["username"],

        "full_name": user["full_name"],

        "role": user["role"]

    }

# ==========================================================
# Current User
# ==========================================================

def get_current_user(

    token: str = Depends(

        oauth2_scheme

    )

):

    payload = decode_token(token)

    if payload is None:

        raise HTTPException(

            status_code=401,

            detail="Invalid Token"

        )

    username = payload.get("sub")

    user = get_user(username)

    if user is None:

        raise HTTPException(

            status_code=401,

            detail="User Not Found"

        )

    return user

# ==========================================================
# Admin Required
# ==========================================================

def admin_required(

    user=Depends(

        get_current_user

    )

):

    if user["role"] != "admin":

        raise HTTPException(

            status_code=403,

            detail="Administrator Access Required"

        )

    return user