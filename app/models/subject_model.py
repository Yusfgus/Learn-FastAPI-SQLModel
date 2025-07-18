from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

from app.schemas.subject_schema import SubjectBase


if TYPE_CHECKING:
    from app.models.student_model import Student  # Import only for type checking to avoid circular imports


# SQLModel model for StudentSubjectLink, representing the many-to-many relationship between Student and Subject
class StudentSubjectLink(SubjectBase, SQLModel, table=True):
    __tablename__ = 'StudentSubjectLink'  # Table name for SQLModel

    student_id: int = Field(foreign_key='StudentTable.id', primary_key=True)
    subject_id: int = Field(foreign_key='SubjectTable.id', primary_key=True)

    # grade : float | None = None

    # # Relationships back to Student and Subject
    # student: Optional['Student'] = Relationship(back_populates='subject_link')
    # subject: Optional['Subject'] = Relationship(back_populates='student_link')


# SQLModel model for Subject
class Subject(SubjectBase, SQLModel, table=True):
    __tablename__ = 'SubjectTable'  # Table name for SQLModel
    
    id: int = Field(default=None, primary_key=True)  # Subject ID, primary key

    # # Many-to-many relationship to Student
    students: list['Student'] = Relationship(back_populates='subjects', link_model=StudentSubjectLink)
    # student_link: list['StudentSubjectLink'] = Relationship(back_populates='subject')
