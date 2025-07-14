from sqlmodel import Field, SQLModel, Relationship

from app.schemas.student_schema import StudentBase
from app.models.subject_model import Subject, StudentSubjectLink
from app.models.GP_model import GP
from app.models.email_model import Email


# SQLModel model for Student
class Student(StudentBase, SQLModel, table=True):
    __tablename__ = 'StudentTable'  # Table name for SQLModel

    id: int = Field(default=None, primary_key=True)  # Student ID, primary key

    # Many-to-many relationship to Subject
    subjects: list[Subject] = Relationship(back_populates='students', link_model=StudentSubjectLink)
    # subject_link: list[StudentSubjectLink] = Relationship(back_populates='student')

    # One-to-one relationship to Graduation Project
    graduation_project: GP | None = Relationship(back_populates='student')

    # Many-to-one relationship to Email
    emails: list[Email] = Relationship(back_populates='student', passive_deletes="all")