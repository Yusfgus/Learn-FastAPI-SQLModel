from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from app.schemas.student_schema import StudentPublic  # Import only for type checking to avoid circular imports


class EmailBase(BaseModel):
    email: str
    # password: str


# SQLModel model for Email Public
class EmailPublic(EmailBase):
    id: int
    student_id: int
    hashed_password: str

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class EmailPublicWithStudent(EmailPublic):
    student: Optional["StudentPublic"] = None  # Student relationship, can be None

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class EmailPublicWithAll(EmailPublicWithStudent):

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


# SQLModel model for Email create
class EmailCreate(EmailBase):
    model_config = {"extra": "forbid"}

    password: str


class EmailLogin(BaseModel):
    email: str
    password: str


# SQLModel model for Email update
class EmailUpdate(BaseModel):    
    email: str | None = None
    password: str | None = None


def rebuild_models():
    # Lazy runtime import to avoid circular import
    from app.schemas.student_schema import StudentPublic

    # Now that StudentPublic is defined, rebuild the models
    EmailPublicWithStudent.model_rebuild()
    EmailPublicWithAll.model_rebuild()

    print("Email models rebuild successfully")
