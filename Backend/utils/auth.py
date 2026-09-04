import jwt
from Backend.config import JWT_SECRET, JWT_ALGORITHM
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials              #OAuth2PasswordBearer
from Backend.database.connection import get_db


security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_db)
):

    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET,
            algorithms = [JWT_ALGORITHM]
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid or expired token"
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    cursor = db.cursor()

    cursor.execute(
        "Select user_id, username, email from users where user_id = (%s)", (user_id, )
    )

    user = cursor.fetchone()

    cursor.close()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "User not Found"
        )


    return user