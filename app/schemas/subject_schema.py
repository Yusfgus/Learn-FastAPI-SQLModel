from pydantic import BaseModel
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.schemas.student_schema import StudentPublic  # Import only for type checking to avoid circular imports


# SQLModel model for Subject base
class SubjectBase(BaseModel):
    name: str
    hours: int


# SQLModel model for Subject create
class SubjectCreate(SubjectBase):
    model_config = {"extra": "forbid"}


# SQLModel model for Subject Public
class SubjectPublic(SubjectBase):
    id: int

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class SubjectPublicWithStudents(SubjectPublic):
    students: list['StudentPublic'] = []  # Students relationship, can be empty

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class SubjectPublicWithAll(SubjectPublicWithStudents):
    
    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


def rebuild_models():
    # Lazy runtime import to avoid circular import
    from app.schemas.student_schema import StudentPublic

    # Now that StudentPublic is defined, rebuild the models
    SubjectPublicWithStudents.model_rebuild()
    SubjectPublicWithAll.model_rebuild()

    print("Subject models rebuild successfully")