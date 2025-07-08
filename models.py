from enum import Enum
from pydantic import BaseModel, field_validator
from sqlmodel import Field, SQLModel, Relationship


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
    student_id: int = Field(foreign_key='StudentTable.id', unique=True)  # Foreign key to Student


# SQLModel model for Graduation project
class GP(GPBase, table=True):
    __tablename__ = 'GPTable'  # Table name for SQLModel

    id: int = Field(default=None, primary_key=True)  # Project ID, primary key
    # Relationship to Student
    student_rl: 'Student' = Relationship(back_populates='gp_rl')


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
    # subjects_rl: list[Subject] = Relationship(back_populates='students_rl')
    # Relationship to Graduation Project
    gp_rl: GP | None = Relationship(back_populates='student_rl')


# SQLModel model for Student create
class StudentCreate(StudentBase):
    # subjects: list[SubjectBase] | None = None
    graduation_project: GPBase | None = None

    @field_validator('department', mode='before')
    @classmethod
    def title_case_dept(cls, value):
        return value.title()
