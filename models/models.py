from enum import Enum
from pydantic import BaseModel, field_validator
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


# SQLModel model for StudentSubjectLink, representing the many-to-many relationship between Student and Subject
class StudentSubjectLink(SQLModel, table=True):
    __tablename__ = 'StudentSubjectLink'  # Table name for SQLModel

    student_id: int = Field(foreign_key='StudentTable.id', primary_key=True)
    subject_id: int = Field(foreign_key='SubjectTable.id', primary_key=True)

    # grade : float | None = None

    # # Relationships back to Student and Subject
    # student: Optional['Student'] = Relationship(back_populates='subject_link')
    # subject: Optional['Subject'] = Relationship(back_populates='student_link')


# SQLModel model for Subject base
class SubjectBase(SQLModel):
    name: str
    hours: int


# SQLModel model for Subject
class Subject(SubjectBase, table=True):
    __tablename__ = 'SubjectTable'  # Table name for SQLModel
    
    id: int = Field(default=None, primary_key=True)  # Subject ID, primary key

    # # Many-to-many relationship to Student
    students: list['Student'] = Relationship(back_populates='subjects', link_model=StudentSubjectLink)
    # student_link: list['StudentSubjectLink'] = Relationship(back_populates='subject')


# SQLModel model for Subject create
class SubjectCreate(SubjectBase):
    pass


# SQLModel model for Subject Public
class SubjectPublic(SubjectBase):
    id: int

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class SubjectPublicWithStudents(SubjectPublic):
    students: list['StudentPublic'] = []  # Students relationship, can be empty

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class SubjectPublicWithAll(SubjectPublicWithStudents):
    
    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================


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


class GPPublic(GPBase):
    id: int
    student_id: int | None

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class GPPublicWithStudent(GPPublic):
    student: Optional["StudentPublic"] = None  # Student relationship, can be None

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class GPPublicWithAll(GPPublicWithStudent):

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================

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


# SQLModel model for Email Public
class EmailPublic(EmailBase):
    id: int
    student_id: int
    hashed_password: str

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class EmailPublicWithStudent(EmailPublic):
    student: Optional["StudentPublic"] = None  # Student relationship, can be None

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class EmailPublicWithAll(EmailPublicWithStudent):

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


# SQLModel model for Email create
class EmailCreate(EmailBase):
    password: str


class EmailLogin(SQLModel):
    email: str
    password: str


# SQLModel model for Email update
class EmailUpdate(SQLModel):    
    email: str | None = None
    password: str | None = None



from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using a secure hashing algorithm."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)



#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================



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

