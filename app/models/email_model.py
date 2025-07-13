from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .student_model import Student, StudentPublic  # Import only for type checking to avoid circular imports


class EmailBase(SQLModel):
    email: str
    # password: str


# SQLModel model for Email
class Email(EmailBase, table=True):
    __tablename__ = 'EmailTable'  # Table name for SQLModel

    id: int = Field(default=None, primary_key=True)  # Email ID, primary key
    hashed_password: str = Field()  # Hashed password

    # One-to-one relationship to Student
    student_id: int | None = Field(default=None, foreign_key='StudentTable.id', ondelete="CASCADE")
    student: Optional["Student"] = Relationship(back_populates='emails')


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
    password: str


class EmailLogin(SQLModel):
    email: str
    password: str


# SQLModel model for Email update
class EmailUpdate(SQLModel):    
    email: str | None = None
    password: str | None = None


def rebuld_models():
    # Lazy runtime import to avoid circular import
    from .student_model import StudentPublic

    # Now that StudentPublic is defined, rebuild the models
    EmailPublicWithStudent.model_rebuild()
    EmailPublicWithAll.model_rebuild()

    print("Email models rebuld successfully")
