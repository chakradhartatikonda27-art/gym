from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import async_session_factory
from app.core.security import decode_access_token
from app.schemas.auth import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user_payload(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    payload_dict = decode_access_token(token)
    if not payload_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenPayload(
        sub=payload_dict.get("sub"),
        role=payload_dict.get("role"),
        tenant_id=payload_dict.get("tenant_id"),
        branch_id=payload_dict.get("branch_id"),
        exp=payload_dict.get("exp")
    )

async def get_db_with_tenant(
    token_payload: TokenPayload = Depends(get_current_user_payload)
) -> AsyncGenerator[AsyncSession, None]:
    """
    Yields an AsyncSession configured with the active tenant_id and branch_id
    to enforce PostgreSQL Row-Level Security (RLS).
    """
    async with async_session_factory() as session:
        # Enforce multi-tenancy at database session level
        await session.execute(
            text("SET LOCAL app.current_tenant_id = :tenant_id;"),
            {"tenant_id": token_payload.tenant_id}
        )
        if token_payload.branch_id:
            await session.execute(
                text("SET LOCAL app.current_branch_id = :branch_id;"),
                {"branch_id": token_payload.branch_id}
            )
        try:
            yield session
        finally:
            await session.close()
