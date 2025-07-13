from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .student_model import Student, StudentPublic  # Import only for type checking to avoid circular imports


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


def rebuld_models():
    # Lazy runtime import to avoid circular import
    from .student_model import StudentPublic

    # Now that StudentPublic is defined, rebuild the models
    SubjectPublicWithStudents.model_rebuild()
    SubjectPublicWithAll.model_rebuild()

    print("Subject models rebuld successfully")