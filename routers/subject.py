from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from sqlmodel import Session, select
from ..db import get_session
from ..dependencies import CommonQueryParams
from ..models.all_models import Subject, SubjectCreate, SubjectPublic, SubjectPublicWithAll


router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
)


@router.get("/", response_model=list[SubjectPublic])
def get_subjects(
    commons: Annotated[CommonQueryParams, Depends()],
    session: Session = Depends(get_session),
) -> list[SubjectPublic]:
    
    statement = select(Subject).offset(commons.skip).limit(commons.limit)
    subjects = session.exec(statement).all()

    return subjects


@router.get("/{subject_id}", response_model=SubjectPublicWithAll)
def get_subject_by_id(
    subject_id: Annotated[int, Path(title="Subject ID")],
    session: Session = Depends(get_session),
) -> Subject:
    
    subject = session.get(Subject, subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject


@router.post("/add", response_model=SubjectPublicWithAll)
def add_subject(
    subject_data: SubjectCreate,
    session: Session = Depends(get_session),
) -> Subject:
    
    subject = Subject.model_validate(subject_data)

    session.add(subject)
    session.commit()
    session.refresh(subject)

    return subject

