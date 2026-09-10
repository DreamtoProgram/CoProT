from fastapi import APIRouter, Depends, HTTPException, status
from Backend.utils.security import (
    create_access_token,
    hash_password,
    verify_password
)
from Backend.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from Backend.database.connection import get_db
from Backend.utils.auth import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/register",
    response_model= UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data : UserCreate,
    db = Depends(get_db)
):
    
    cursor = db.cursor()

    cursor.execute(
        'select user_id from users where email = %s', (user_data.email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    else:

        hashed_password = hash_password(user_data.password)

        cursor.execute(
                    """
                    INSERT INTO users
                    (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        user_data.username,
                        user_data.email,
                        hashed_password
                    )
                )

        db.commit()

        user_id = cursor.lastrowid
        cursor.close()

        return {
            "user_id": user_id,
            "username": user_data.username,
            "email": user_data.email
        }


@router.post(
    '/login',
    response_model= TokenResponse
)
def user_login(user_data : UserLogin, db = Depends(get_db)):
        cursor = db.cursor()

        cursor.execute(
            "SELECT user_id, username, email, password_hash FROM users WHERE email = %s", (user_data.email,)
        )

        user_ = cursor.fetchone()
        cursor.close()

        if not user_:
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="User Not Found"
            )

        if not verify_password(user_data.password, user_["password_hash"]):
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Email or Password"
            )

        access_token = create_access_token(user_["user_id"])

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
     return current_user

