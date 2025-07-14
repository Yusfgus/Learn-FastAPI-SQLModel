from enum import Enum
from pydantic import BaseModel, field_validator

from app.schemas.subject_schema import SubjectPublic
from app.schemas.GP_schema import GPPublic, GPCreate
from app.schemas.email_schema import EmailPublic


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
class StudentBase(BaseModel):
    name: str 
    age: int
    department: Department 


# SQLModel model for Student create
class StudentCreate(StudentBase):
    model_config = {"extra": "forbid"}

    # subjects: list[SubjectBase] | None = None
    graduation_project: GPCreate | None = None

    @field_validator('department', mode='before')
    @classmethod
    def lower_case_dept(cls, value):
        return value.lower()


# SQLModel model for Student update
class StudentUpdate(BaseModel):
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

