from typing import Annotated
from fastapi import Depends, Path, APIRouter, HTTPException
from sqlmodel import Session, select

from app.db import db_dependency
from app.dependencies import CommonQueryParams
from app.models.email_model import Email, EmailPublic, EmailPublicWithAll
from app.routers.auth import get_current_email


router = APIRouter(
    prefix="/emails",
    tags=["emails"],
)


@router.get("/", response_model=list[EmailPublic])
def get_emails(
    commons: Annotated[CommonQueryParams, Depends()],
    session: db_dependency,
    email: Annotated[Email, Depends(get_current_email)],
) -> list[Email]:
    
    statement = select(Email).offset(commons.skip).limit(commons.limit)
    emails = session.exec(statement).all()

    return emails


@router.get("/{email_id}", response_model=EmailPublicWithAll)
def get_email_by_id(
    email_id: Annotated[int, Path(title="Email ID")],
    session: db_dependency,
    email: Annotated[Email, Depends(get_current_email)],
) -> Email:
    
    email = session.get(Email, email_id)
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")

    return email


