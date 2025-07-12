from enum import Enum
from pydantic import BaseModel, field_validator
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from models.subject_model import Subject, StudentSubjectLink, SubjectPublic
from models.GP_model import GP, GPPublic, GPCreate
from models.email_model import Email, EmailPublic


# Enum for allowed departement types
class Department(str, Enum):
    cs = 'cs'  # Computer Science
    # is = 'is'  # Information Systems
    sc = 'sc'  # Sientific Computing
    csys = 'csys'  # Computer Systems

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


# SQLModel model for Student base
class StudentBase(SQLModel):
    name: str 
    age: int
    department: Department 


# SQLModel model for Student
class Student(StudentBase, table=True):
    __tablename__ = 'StudentTable'  # Table name for SQLModel

    id: int = Field(default=None, primary_key=True)  # Student ID, primary key

    # Many-to-many relationship to Subject
    subjects: list[Subject] = Relationship(back_populates='students', link_model=StudentSubjectLink)
    # subject_link: list[StudentSubjectLink] = Relationship(back_populates='student')

    # One-to-one relationship to Graduation Project
    graduation_project: GP | None = Relationship(back_populates='student')

    # Many-to-one relationship to Email
    emails: list[Email] = Relationship(back_populates='student', cascade_delete=True)



# SQLModel model for Student create
class StudentCreate(StudentBase):
    # subjects: list[SubjectBase] | None = None
    graduation_project: GPCreate | None = None

    @field_validator('department', mode='before')
    @classmethod
    def lower_case_dept(cls, value):
        return value.lower()


# SQLModel model for Student update
class StudentUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    department: Department | None = None

    @field_validator('department', mode='before')
    @classmethod
    def lower_case_dept(cls, value):
        return value.lower() if value else value
    

# SQLModel model for Student Public
class StudentPublic(StudentBase):
    id: int

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class StudentPublicWithGP(StudentPublic):
    graduation_project: GPPublic | None = None  # Graduation project relationship, can be None

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class StudentPublicWithEmails(StudentPublic):
    emails: list[EmailPublic] = []  # Emails relationship, can be empty

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class StudentPublicWithSubjects(StudentPublic):
    subjects: list[SubjectPublic] = []  # Subjects relationship, can be empty

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class StudentPublicWithAll(StudentPublicWithGP, StudentPublicWithEmails, StudentPublicWithSubjects):
    """
    This model combines all public details of a student including graduation project,
    emails, and subjects.
    """

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel
