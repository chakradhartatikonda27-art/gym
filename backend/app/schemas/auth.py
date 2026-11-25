from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    full_name: str
    role: str
    tenant_id: str
    branch_id: Optional[str] = None

class TokenPayload(BaseModel):
    sub: str                  # user_id
    role: str
    tenant_id: str
    branch_id: Optional[str] = None
    exp: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
