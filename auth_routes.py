"""
auth_routes.py

Authentication API Routes
"""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.auth import (
    authenticate_user,
    get_current_user,
    admin_required
)

from backend.users import (
    list_users
)

from fastapi import Depends, HTTPException

router = APIRouter(
    tags=["Authentication"]
)

# ==========================================================
# Request Model
# ==========================================================

class LoginRequest(BaseModel):

    username: str

    password: str

# ==========================================================
# Login
# ==========================================================

@router.post("/login")

def login(data: LoginRequest):

    result = authenticate_user(

        data.username,

        data.password

    )

    if result is None:

        raise HTTPException(

            status_code=401,

            detail="Invalid username or password"

        )

    return result

# ==========================================================
# Current User
# ==========================================================

@router.get("/me")

def me(

    user=Depends(get_current_user)

):

    return {

        "username": user["username"],

        "full_name": user["full_name"],

        "role": user["role"]

    }

# ==========================================================
# Admin Only
# ==========================================================

@router.get("/users")

def users(

    user=Depends(admin_required)

):

    return {

        "users": list_users()

    }

# ==========================================================
# Health Check
# ==========================================================

@router.get("/auth-status")

def auth_status():

    return {

        "status": "Authentication API Running"

    }