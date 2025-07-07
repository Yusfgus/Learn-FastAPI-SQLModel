from enum import Enum
from pydantic import BaseModel


# Enum for allowed departement types
class Departement(Enum):
    CS = 'cs'  # Computer Science
    IS = 'is'  # Information Systems
    SC = 'sc'  # Sientific Computing
    CSys = 'csys'  # Computer Systems


# Pydantic model for Subject
class Subject(BaseModel):
    id: int
    name: str
    hours: int


# Pydantic model for Student
class Student(BaseModel):
    id: int
    name: str
    age: int
    departement: str
    subjects: list[Subject] = []  # List of subjects, default is empty list

