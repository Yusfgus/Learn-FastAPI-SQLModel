from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.student_model import Student, StudentPublic  # Import only for type checking to avoid circular imports


# SQLModel model for Graduation project base
class GPBase(SQLModel):
    title: str
    description: str


# SQLModel model for Graduation project
class GP(GPBase, table=True):
    __tablename__ = 'GPTable'

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign key to student
    student_id: int | None = Field(default=None, foreign_key='StudentTable.id', unique=True, ondelete="SET NULL")

    # Relationship back to student
    student: Optional["Student"] = Relationship(back_populates='graduation_project')


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
    from .student_model import StudentPublic

    # Now that StudentPublic is defined, rebuild the models
    GPPublicWithStudent.model_rebuild()
    GPPublicWithAll.model_rebuild()

    print("GP models rebuild successfully")
