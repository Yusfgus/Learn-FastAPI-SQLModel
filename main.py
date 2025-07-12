from fastapi import Body, FastAPI, HTTPException, Query, Path, Depends
from typing import Annotated
from models.models import *
# from models.GP_model import GP, GPCreate, GPPublicWithAll, GPPublic
# from models.email_model import Email, EmailBase, EmailCreate, EmailPublic, EmailPublicWithAll, EmailUpdate, hash_password, verify_password
# from models.subject_model import Subject, SubjectCreate, SubjectPublicWithAll, SubjectPublic
# from models.student_model import Student, StudentCreate, StudentPublicWithEmails, StudentPublicWithGP, StudentUpdate, StudentPublic, Department, StudentPublicWithAll
from db import init_db, get_session, drop_table
from sqlmodel import Session, select
from HelperFunctions import hash_password, verify_password


# Initialize the database
if __name__ == "__main__":
    print("run main.py")
    # Initialize the database when running this script directly
    # drop_table(table=Email)
    init_db()


# # Create FastAPI app instance
app = FastAPI()


# @app.on_event("startup")
# def on_startup():
#     print("Starting up the FastAPI application...")


# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}


# About endpoint
@app.get("/about")
def about() -> str:
    return "This is the about page"


# Add 50 to a given number via query parameter
@app.get("/add 50")
def add_50(num: int) -> int:
    return num + 50


class CommonQueryParams:
    def __init__(
            self, q: str | None = None, 
            skip: Annotated[int, Field(ge=0)] = 0, 
            limit: Annotated[int, Field(gt=0, le=100)] = 100
    ):
        self.q = q
        self.skip = skip
        self.limit = limit


# Endpoint to get all students or filter by department or age or id
@app.get("/students", response_model=list[StudentPublic])
def get_students(
    commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)],
    department: Department | None = None,
    age: Annotated[int | None, Query(gt=0, le=100)] = None,
    session: Session = Depends(get_session),
) -> list[Student]:
    
    statement = select(Student)

    if department is not None:
        # If department is provided, filter the student list
        statement = statement.where(Student.department == department)

    if age is not None:
        # If age is provided, filter the student list
        statement = statement.where(Student.age == age) 

    statement = statement.offset(commons.skip)

    statement = statement.limit(commons.limit)

    # Execute the query and return the results
    filtered_students = session.exec(statement).all()

    return filtered_students


# Endpoint to get a single student by id
@app.get("/students/{student_id}", response_model=StudentPublicWithAll)
def get_student_by_id(
    student_id: Annotated[int, Path(title="Student ID")],
    session: Session = Depends(get_session),
) -> Student:
    
    student = session.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    return student


# # Endpoint to get students by department type
# @app.get("/departments")
# def get_all_department() -> list[str]:
#     return Department.__members__.keys()


@app.post("/students/add", response_model=StudentPublicWithGP)
def add_student(
    student_data: StudentCreate,
    session: Session = Depends(get_session),
) -> Student:

    '''
    Notice that:
        we can create the student first then pass it as a parameter to the GP relationship,
        or we can create the GP first and pass it as a parameter to the student relationship
    '''

    gp_obj = GP(
        title=student_data.graduation_project.title,
        description=student_data.graduation_project.description,
        # student_id=student_obj.id,  # No need to set student_id here, it will be set automatically
    ) if student_data.graduation_project else None

    student_obj = Student(
        name=student_data.name,
        age=student_data.age,
        department=student_data.department,
        graduation_project=gp_obj,  # Set the GP object if provided
    )
    session.add(student_obj)
    session.commit()

    # session.refresh(student_obj)  # Refresh the student object to get the updated data
    # print("======== New student: ", student_obj)

    return student_obj


# update student by id
@app.patch("/students/{student_id}", response_model=StudentPublic)
def update_student(
    student_id: Annotated[int, Path(title="Student ID")],
    new_student: StudentUpdate,
    session: Session = Depends(get_session),
) -> Student:

    student_db = session.get(Student, student_id)
    if student_db is None:
        raise HTTPException(status_code=404, detail="student not found")

    student_data = new_student.model_dump(exclude_unset=True)
    student_db.sqlmodel_update(student_data)

    session.add(student_db)
    session.commit()
    session.refresh(student_db)

    return student_db


# delete student by id
@app.delete("/students/{student_id}", response_model=dict[str, str | StudentPublic])
def delete_student(
    student_id: Annotated[int, Path(title="Student ID")],
    session: Session = Depends(get_session),
) -> dict:
    
    student = session.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    # student_Public = StudentPublic(student=student)

    session.delete(student)
    session.commit()

    return {
        "student": student,
        "message": "student deleted successfully"
    }


# get all graduation projects
@app.get("/GP", response_model=list[GPPublic])
def get_graduation_projects(
    commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)],
    session: Session = Depends(get_session),
) -> list[GP]:
    
    statement = select(GP).offset(commons.skip).limit(commons.limit)
    graduation_projects = session.exec(statement).all()

    return graduation_projects


# get graduation project by id
@app.get("/GP/{gp_id}", response_model=GPPublicWithAll)
def get_graduation_project_by_id(
    gp_id: Annotated[int, Path(title="Graduation Project ID")],
    session: Session = Depends(get_session),
) -> GP:
    
    graduation_project = session.get(GP, gp_id)
    if graduation_project is None:
        raise HTTPException(status_code=404, detail="Graduation project not found")

    return graduation_project


@app.put("/students/{student_id}/emails/add", response_model=EmailPublicWithAll)
def add_student_email(
    student_id: Annotated[int, Path(title="Student ID")],
    email_data: EmailCreate,
    session: Session = Depends(get_session),
) -> Email:
    
    student = session.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    # Hash the password before saving
    plain_password = email_data.password
    hashed_password = hash_password(plain_password)
    extra_data = {"hashed_password": hashed_password}

    email = Email.model_validate(email_data, update=extra_data)
    student.emails.append(email)

    # session.add(email)
    session.add(student)
    session.commit()

    return email


# Endpoint for logging in a student
@app.post("/students/{student_id}/login")
def student_login(
    email_data: EmailCreate,
    session: Session = Depends(get_session),
) -> dict[str, str]:
    
    email_db = session.exec(select(Email).where(Email.email == email_data.email)).first()
    if email_db is None:
        raise HTTPException(status_code=404, detail="Email not found")
    
    if not verify_password(plain_password=email_data.password, hashed_password=email_db.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password")
    
    student = session.get(Student, email_db.student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Email found but Student not found")

    return {"message": "Login successful", "student": student.name}


@app.get("/emails", response_model=list[EmailPublic])
def get_emails(
    commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)],
    session: Session = Depends(get_session),
) -> list[Email]:
    
    statement = select(Email).offset(commons.skip).limit(commons.limit)
    emails = session.exec(statement).all()

    return emails


@app.get("/emails/{email_id}", response_model=EmailPublicWithAll)
def get_email_by_id(
    email_id: Annotated[int, Path(title="Email ID")],
    session: Session = Depends(get_session),
) -> Email:
    
    email = session.get(Email, email_id)
    if email is None:
        raise HTTPException(status_code=404, detail="Email not found")

    return email


@app.get("/subjects", response_model=list[SubjectPublic])
def get_subjects(
    commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)],
    session: Session = Depends(get_session),
) -> list[SubjectPublic]:
    
    statement = select(Subject).offset(commons.skip).limit(commons.limit)
    subjects = session.exec(statement).all()

    return subjects


@app.get("/subjects/{subject_id}", response_model=SubjectPublicWithAll)
def get_subject_by_id(
    subject_id: Annotated[int, Path(title="Subject ID")],
    session: Session = Depends(get_session),
) -> Subject:
    
    subject = session.get(Subject, subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject


@app.post("/subjects/add", response_model=SubjectPublicWithAll)
def add_subject(
    subject_data: SubjectCreate,
    session: Session = Depends(get_session),
) -> Subject:
    
    subject = Subject.model_validate(subject_data)

    session.add(subject)
    session.commit()
    session.refresh(subject)

    return subject


@app.patch("/students_subjects")
def add_subject_to_student(
    student_id: Annotated[int, Body(title="Student ID")],
    subject_id: Annotated[int, Body(title="Subject ID")],
    session: Session = Depends(get_session),
) -> dict:
    
    student = session.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    subject = session.get(Subject, subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="subject not found")

    # Check if the subject is already added to the student
    if subject in student.subjects:
        raise HTTPException(status_code=400, detail="Subject already added to student")
    
    student.subjects.append(subject)
    session.add(student)
    session.commit()

    return {
        "message": f"Subject \'{subject.name}\' added to student \'{student.name}\' successfully"
    }


@app.get("/students/{student_id}/subjects", response_model=list[SubjectPublic])
def get_student_subjects(
    student_id: Annotated[int, Path(title="Student ID")],
    session: Session = Depends(get_session),
) -> list[Subject]:
    
    student = session.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    return student.subjects

print("============= Every thing's good ================")