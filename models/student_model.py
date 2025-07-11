from enum import Enum
from pydantic import BaseModel, field_validator
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from models.subject_model import Subject, StudentSubjectLink, SubjectBase, SubjectRead
from models.GP_model import GP, GPBase, GPRead
from models.email_model import Email, EmailRead


# Enum for allowed departement types
class Department(Enum):
    CS = 'cs'  # Computer Science
    IS = 'is'  # Information Systems
    SC = 'sc'  # Sientific Computing
    CSys = 'csys'  # Computer Systems


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
    graduation_project: GPBase | None = None

    @field_validator('department', mode='before')
    @classmethod
    def lower_case_dept(cls, value):
        return value.lower()


# SQLModel model for Student update
class StudentUpdate(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    department: Optional[Department] = None

    @field_validator('department', mode='before')
    @classmethod
    def lower_case_dept(cls, value):
        return value.lower() if value else value
    

# SQLModel model for Student read
class StudentRead(StudentBase):
    id: int
    # subjects: list[SubjectRead] = []  # Subjects relationship, can be empty
    graduation_project: Optional[GPRead] = None  # Graduation project relationship, can be None
    emails: list[EmailRead] = []  # Emails relationship, can be empty

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with SQLModel

    def __init__(self, student: Student):
        super().__init__(
            name=student.name, 
            age=student.age, 
            department=student.department, 
            id=student.id, 
            graduation_project=student.graduation_project,
            emails=student.emails,
        )
