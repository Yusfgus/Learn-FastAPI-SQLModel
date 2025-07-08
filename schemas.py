from enum import Enum
from pydantic import BaseModel, validator


# Enum for allowed departement types
class Departement(Enum):
    CS = 'cs'  # Computer Science
    IS = 'is'  # Information Systems
    SC = 'sc'  # Sientific Computing
    CSys = 'csys'  # Computer Systems


# Pydantic model for Subject
class Subject(BaseModel):
    name: str
    hours: int


# Pydantic model for Student
class StudentBase(BaseModel):
    name: str
    age: int
    departement: str
    subjects: list[Subject] = []  # List of subjects, default is empty list


from pydantic import field_validator

class StudentCreate(StudentBase):
    @field_validator('departement', mode='before')
    @classmethod
    def title_case_dept(cls, value):
        return value.title()


class StudentWithID(StudentBase):
    id: int
