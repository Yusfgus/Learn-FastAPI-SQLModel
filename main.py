from fastapi import FastAPI, HTTPException, Query, Path, Depends
from typing import Annotated
from models import *  # Ensure StudentUpdate is defined in models.py or import it directly
from db import init_db, get_session, drop_table
from sqlmodel import Session, select


# Initialize the database
if __name__ == "__main__":
    print("run main.py")
    # Initialize the database when running this script directly
    drop_table(table=Email)
    init_db()


# # Create FastAPI app instance
app = FastAPI()


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


# Endpoint to get all students or filter by department or age or id
@app.get("/students", response_model=list[StudentRead])
def get_students(
    id: Annotated[int | None, Query(gt=0)] = None,
    department: Department | None = None,
    age: Annotated[int | None, Query(gt=0, le=100)] = None,
    limit: Annotated[int | None, Query(gt=0)] = None,
    skip: Annotated[int | None, Query(gt=0)] = None,
    session: Session = Depends(get_session),
) -> list[Student]:
    
    statement = select(Student)

    if id is not None:
        # If id is provided, filter the student list
        statement = statement.where(Student.id == id)

    if department is not None:
        # If department is provided, filter the student list
        statement = statement.where(Student.department == department)

    if age is not None:
        # If age is provided, filter the student list
        statement = statement.where(Student.age == age) 

    if skip is not None:
        # If skip is provided, apply the skip to the student list
        statement = statement.offset(skip)

    if limit is not None:
        # If limit is provided, apply the limit to the student list
        statement = statement.limit(limit)

    # Execute the query and return the results
    filtered_students = session.exec(statement).all()

    return filtered_students


# Endpoint to get a single student by id
@app.get("/students/{student_id}", response_model=StudentRead)
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


@app.post("/students/add", response_model=StudentRead)
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
@app.put("/students/{student_id}", response_model=StudentRead)
def update_student(
    student_id: Annotated[int, Path(title="Student ID")],
    student_data: StudentUpdate,
    session: Session = Depends(get_session),
) -> Student:

    student = session.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    # Update the student's attributes
    if student_data.name is not None:
        student.name = student_data.name
    if student_data.age is not None:
        student.age = student_data.age
    if student_data.department is not None:
        student.department = student_data.department

    session.add(student)
    session.commit()
    session.refresh(student)

    return student


# delete student by id
@app.delete("/students/{student_id}", response_model=dict[str, str | StudentRead])
def delete_student(
    student_id: Annotated[int, Path(title="Student ID")],
    session: Session = Depends(get_session),
) -> dict:
    
    student = session.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    # student_read = StudentRead(student=student)

    session.delete(student)
    session.commit()

    return {
        "student": student,
        "message": "student deleted successfully"
    }


# get all graduation projects
@app.get("/GP", response_model=list[GPRead])
def get_graduation_projects(
    session: Session = Depends(get_session),
) -> list[GP]:
    
    statement = select(GP)
    graduation_projects = session.exec(statement).all()

    return graduation_projects


@app.put("/students/{student_id}/emails/add", response_model=EmailRead)
def update_student_email(
    student_id: Annotated[int, Path(title="Student ID")],
    email_data: EmailBase,
    session: Session = Depends(get_session),
) -> Email:
    
    student = session.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    email = Email(
        email=email_data.email,
        password=email_data.password,
        student_id=student.id,  # Associate the email with the student
    )

    student.emails.append(email)
    # session.add(email)
    session.add(student)
    session.commit()

    return email


@app.get("/emails", response_model=list[EmailRead])
def get_emails(
    session: Session = Depends(get_session),
) -> list[EmailRead]:
    
    statement = select(Email)
    emails = session.exec(statement).all()

    return emails


print("============= Every thing's good ================")