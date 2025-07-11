from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from models.student_model import Student  # Import only for type checking to avoid circular imports

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
    pass


class GPRead(GPBase):
    id: int
    student_id: Optional[int] = None  # Student ID, can be None if not assigned

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with SQLModel

