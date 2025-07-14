from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from sqlmodel import select

from app.core.dependencies import CommonQueryParams, db_dependency

from app.models.email_model import Email
from app.models.subject_model import Subject

from app.schemas.subject_schema import SubjectCreate, SubjectPublic, SubjectPublicWithAll

from app.routers.auth import get_current_email


router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
)


@router.get("/", response_model=list[SubjectPublic])
def get_subjects(
    commons: Annotated[CommonQueryParams, Depends()],
    session: db_dependency,
    email: Annotated[Email, Depends(get_current_email)],
) -> list[SubjectPublic]:
    
    statement = select(Subject).offset(commons.skip).limit(commons.limit)
    subjects = session.exec(statement).all()

    return subjects


@router.get("/{subject_id}", response_model=SubjectPublicWithAll)
def get_subject_by_id(
    subject_id: Annotated[int, Path(title="Subject ID")],
    session: db_dependency,
) -> Subject:
    
    subject = session.get(Subject, subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject


@router.post("/add", response_model=SubjectPublicWithAll)
def add_subject(
    subject_data: SubjectCreate,
    session: db_dependency,
) -> Subject:
    
    subject = Subject.model_validate(subject_data)

    session.add(subject)
    session.commit()
    session.refresh(subject)

    return subject

