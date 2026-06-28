"""
user_routes.py

Admin User Management APIs
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.auth import admin_required

from backend.users import (
    list_users,
    add_user,
    delete_user,
    update_password,
    get_user
)

router = APIRouter(
    prefix="/users",
    tags=["User Management"]
)

# ==========================================================
# Models
# ==========================================================

class NewUser(BaseModel):

    username: str

    full_name: str

    password: str

    role: str = "operator"


class PasswordUpdate(BaseModel):

    password: str


# ==========================================================
# List Users
# ==========================================================

@router.get("/")

def get_users(

    admin=Depends(admin_required)

):

    return {

        "users": list_users()

    }


# ==========================================================
# Add User
# ==========================================================

@router.post("/")

def create_user(

    user: NewUser,

    admin=Depends(admin_required)

):

    if get_user(user.username):

        raise HTTPException(

            status_code=400,

            detail="Username already exists."

        )

    add_user(

        user.username,

        user.full_name,

        user.password,

        user.role

    )

    return {

        "message": "User created successfully."

    }


# ==========================================================
# Delete User
# ==========================================================

@router.delete("/{username}")

def remove_user(

    username: str,

    admin=Depends(admin_required)

):

    success = delete_user(username)

    if not success:

        raise HTTPException(

            status_code=400,

            detail="Cannot delete this user."

        )

    return {

        "message": "User deleted successfully."

    }


# ==========================================================
# Reset Password
# ==========================================================

@router.put("/{username}/password")

def reset_password(

    username: str,

    body: PasswordUpdate,

    admin=Depends(admin_required)

):

    if not get_user(username):

        raise HTTPException(

            status_code=404,

            detail="User not found."

        )

    update_password(

        username,

        body.password

    )

    return {

        "message": "Password updated successfully."

    }