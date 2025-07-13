from typing import Annotated
from fastapi import Depends, Path, APIRouter, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..dependencies import CommonQueryParams
from ..models.all_models import Email, EmailPublic, EmailPublicWithAll


router = APIRouter(
    prefix="/emails",
    tags=["emails"],
)


@router.get("/", response_model=list[EmailPublic])
def get_emails(
    commons: Annotated[CommonQueryParams, Depends()],
    session: Session = Depends(get_session),
) -> list[Email]:
    
    statement = select(Email).offset(commons.skip).limit(commons.limit)
    emails = session.exec(statement).all()

    return emails


@router.get("/{email_id}", response_model=EmailPublicWithAll)
def get_email_by_id(
    email_id: Annotated[int, Path(title="Email ID")],
    session: Session = Depends(get_session),
) -> Email:
    
    email = session.get(Email, email_id)
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")

    return email


