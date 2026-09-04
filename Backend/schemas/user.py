from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username : str
    email : EmailStr
    password : str


class UserResponse(BaseModel):
    user_id : int
    username : str
    email : EmailStr

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


