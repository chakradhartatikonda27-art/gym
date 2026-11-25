from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from app.db.session import async_session_factory
from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginRequest, Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest):
    async with async_session_factory() as session:
        # Direct lookup for login before tenant context is set
        stmt = text("""
            SELECT id, tenant_id, branch_id, full_name, role, password_hash, is_active
            FROM users
            WHERE email = :email
        """)
        result = await session.execute(stmt, {"email": credentials.email})
        user = result.fetchone()

        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account")

        # Create JWT token embedded with tenant_id and branch_id
        token_data = {
            "sub": str(user.id),
            "role": str(user.role),
            "tenant_id": str(user.tenant_id),
            "branch_id": str(user.branch_id) if user.branch_id else None
        }
        access_token = create_access_token(data=token_data)

        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=str(user.id),
            full_name=user.full_name,
            role=str(user.role),
            tenant_id=str(user.tenant_id),
            branch_id=str(user.branch_id) if user.branch_id else None
        )
