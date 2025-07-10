from enum import Enum
from pydantic import BaseModel, field_validator
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional

# Enum for allowed departement types
class Department(Enum):
    CS = 'cs'  # Computer Science
    IS = 'is'  # Information Systems
    SC = 'sc'  # Sientific Computing
    CSys = 'csys'  # Computer Systems

# ===== Subject ============================================================================================

# # SQLModel model for Subject base
# class SubjectBase(SQLModel):
#     name: str
#     hours: int
#     student_id: int = Field(foreign_key='student.id')  # Foreign key to Student


# # SQLModel model for Subject
# class Subject(SubjectBase, table=True):
#     id: int = Field(default=None, primary_key=True)  # Subject ID, primary key
#     # Relationship to Student
#     students_rl: list['Student'] = Relationship(back_populates='subjects_rl')
    

# ===== Graduation Project ============================================================================================


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


# ===== Email ============================================================================================


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

# ===== Student ============================================================================================


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
    # subjects_rl: list[Subject] = Relationship(back_populates='students_rl')

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
    # subjects_rl: list[Subject] = []  # Subjects relationship, can be empty
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
