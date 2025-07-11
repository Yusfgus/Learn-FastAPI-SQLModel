from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from models.student_model import Student  # Import only for type checking to avoid circular imports
class EmailBase(SQLModel):
    email: str
    password: str


# SQLModel model for Email
class Email(EmailBase, table=True):
    __tablename__ = 'EmailTable'  # Table name for SQLModel

    id: int = Field(default=None, primary_key=True)  # Email ID, primary key

    # One-to-one relationship to Student
    student_id: int | None = Field(default=None, foreign_key='StudentTable.id', ondelete="CASCADE")
    student: Optional["Student"] = Relationship(back_populates='emails')


# SQLModel model for Email read
class EmailRead(EmailBase):
    id: int
    student_id: Optional[int] = None  # Student ID, can be None if not assigned

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with SQLModel
