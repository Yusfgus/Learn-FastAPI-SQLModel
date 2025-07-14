from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from app.schemas.student_schema import StudentPublic  # Import only for type checking to avoid circular imports


# SQLModel model for Graduation project base
class GPBase(BaseModel):
    title: str
    description: str


class GPCreate(GPBase):
    model_config = {"extra": "forbid"}


class GPPublic(GPBase):
    id: int
    student_id: int | None

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class GPPublicWithStudent(GPPublic):
    student: Optional["StudentPublic"] = None  # Student relationship, can be None

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class GPPublicWithAll(GPPublicWithStudent):

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


def rebuild_models():
    # Lazy runtime import to avoid circular import
    from app.schemas.student_schema import StudentPublic

    # Now that StudentPublic is defined, rebuild the models
    GPPublicWithStudent.model_rebuild()
    GPPublicWithAll.model_rebuild()

    print("GP models rebuild successfully")
