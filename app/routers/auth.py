from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Form, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select
from pydantic import BaseModel

from app.models.email_model import Email
from app.db import db_dependency
from app.security import verify_password, create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix="", 
    tags=["Auth"]
)  # no prefix; /token, /me


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")  # FastAPI helper


class Token(BaseModel):
    access_token: str
    token_type: str


# class TokenData(BaseModel):
#     email: str | None = None


# ── login endpoint (OAuth2 Password flow) ───────────────────────────────────────


def get_email(session: db_dependency, email: str) -> Email:
    return session.exec(select(Email).where(Email.email == email)).first()


def authenticate_user(session: db_dependency, email: str, password: str):
    email_db = get_email(session, email)
    if not email_db:
        return False
    if not verify_password(plain=password, hashed=email_db.hashed_password):
        return False
    return email_db


@router.post("/token")
async def login_for_access_token(
    session: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    email = authenticate_user(session, form_data.username, form_data.password)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
        # {
        #     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ6YWhyYW5AZ21haWwuY29tIiwiZXhwIjoxNzUyNDU0OTE1fQ.d7dZ5U7Vmrn3vS0c9nHda42TLJ8Erkl3K47gyo7de-g",
        #     "token_type": "bearer"
        # }


# ── dependency: get current Email from token ─────────────────────────────────────


def get_current_email(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: db_dependency,
) -> Email:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token=token)
    if not payload:
        print("here 1")
        raise credentials_exception

    email = payload.get("sub")
    if email is None:
        print("here 2")
        raise credentials_exception
    
    # token_data = TokenData(email=email)
    # email_db = get_email(session=session, email=token_data.email)

    email_db = get_email(session=session, email=email)
    if email_db is None:
        print("here 3")
        raise credentials_exception
    
    return email_db


def require_admin(user: Email = Depends(get_current_email)) -> Email:
    if user.role != "admin":
        raise HTTPException(403, detail="Admins only")
    return user
