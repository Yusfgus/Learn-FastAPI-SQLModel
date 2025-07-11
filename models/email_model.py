from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from models.student_model import Student  # Import only for type checking to avoid circular imports


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


# SQLModel model for Email Puplic
class EmailPuplic(EmailBase):
    id: int
    student_id: int
    hashed_password: str

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


# SQLModel model for Email create
class EmailCreate(EmailBase):
    password: str

# SQLModel model for Email update
class EmailUpdate(SQLModel):    
    email: str | None = None
    password: str | None = None

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel



from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using a secure hashing algorithm."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)