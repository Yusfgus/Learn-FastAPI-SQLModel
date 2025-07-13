from typing import Annotated
from fastapi import Depends, Path, APIRouter, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..dependencies import CommonQueryParams
from ..models.GP_model import GP, GPPublic, GPPublicWithAll


router = APIRouter(
    prefix="/GP",
    tags=["graduation projects"],
)


# get all graduation projects
@router.get("/", response_model=list[GPPublic])
def get_graduation_projects(
    commons: Annotated[CommonQueryParams, Depends()],
    session: Session = Depends(get_session),
) -> list[GP]:
    
    statement = select(GP).offset(commons.skip).limit(commons.limit)
    graduation_projects = session.exec(statement).all()

    return graduation_projects


# get graduation project by id
@router.get("/{gp_id}", response_model=GPPublicWithAll)
def get_graduation_project_by_id(
    gp_id: Annotated[int, Path(title="Graduation Project ID")],
    session: Session = Depends(get_session),
) -> GP:
    
    graduation_project = session.get(GP, gp_id)
    if graduation_project is None:
        raise HTTPException(status_code=404, detail="Graduation project not found")

    return graduation_project

