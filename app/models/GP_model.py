from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

from app.schemas.GP_schema import GPBase


if TYPE_CHECKING:
    from app.models.student_model import Student  # Import only for type checking to avoid circular imports


# SQLModel model for Graduation project
class GP(GPBase, SQLModel, table=True):
    __tablename__ = 'GPTable'

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign key to student
    student_id: int | None = Field(default=None, foreign_key='StudentTable.id', unique=True, ondelete="SET NULL")

    # Relationship back to student
    student: Optional["Student"] = Relationship(back_populates='graduation_project')
