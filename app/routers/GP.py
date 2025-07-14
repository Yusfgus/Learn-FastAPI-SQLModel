from typing import Annotated
from fastapi import Depends, Path, APIRouter, HTTPException
from sqlmodel import Session, select

from app.db import db_dependency
from app.dependencies import CommonQueryParams
from app.models.GP_model import GP, GPPublic, GPPublicWithAll
from app.models.email_model import Email
from app.routers.auth import get_current_email


router = APIRouter(
    prefix="/GP",
    tags=["graduation projects"],
)


# get all graduation projects
@router.get("/", response_model=list[GPPublic])
def get_graduation_projects(
    commons: Annotated[CommonQueryParams, Depends()],
    session: db_dependency,
    email: Annotated[Email, Depends(get_current_email)],
) -> list[GP]:
    
    statement = select(GP).offset(commons.skip).limit(commons.limit)
    graduation_projects = session.exec(statement).all()

    return graduation_projects


# get graduation project by id
@router.get("/{gp_id}", response_model=GPPublicWithAll)
def get_graduation_project_by_id(
    gp_id: Annotated[int, Path(title="Graduation Project ID")],
    session: db_dependency,
    email: Annotated[Email, Depends(get_current_email)],
) -> GP:
    
    graduation_project = session.get(GP, gp_id)
    if graduation_project is None:
        raise HTTPException(status_code=404, detail="Graduation project not found")

    return graduation_project

