from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

from app.schemas.email_schema import EmailBase


if TYPE_CHECKING:
    from app.models.student_model import Student  # Import only for type checking to avoid circular imports


# SQLModel model for Email
class Email(EmailBase, SQLModel, table=True):
    __tablename__ = 'EmailTable'  # Table name for SQLModel

    id: int = Field(default=None, primary_key=True)  # Email ID, primary key
    hashed_password: str = Field()  # Hashed password

    # One-to-one relationship to Student
    student_id: int | None = Field(default=None, foreign_key='StudentTable.id', ondelete="CASCADE")
    student: Optional["Student"] = Relationship(back_populates='emails')
