from fastapi import FastAPI, HTTPException, Query, Path, Depends
from typing import Annotated
from models import *
from db import init_db, get_session
from sqlmodel import Session, select


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
@app.get("/students")
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
@app.get("/students/{student_id}")
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


@app.post("/students/add")
def add_student(
    student_data: StudentCreate,
    session: Session = Depends(get_session),
) -> Student:

    student_obj = Student(
        name=student_data.name,
        age=student_data.age,
        department=student_data.department,
    )
    session.add(student_obj)
    session.commit()  # Commit to generate the student ID
    session.refresh(student_obj)  # Refresh to get the generated ID

    if student_data.graduation_project:
        gp_obj = GP(
            title=student_data.graduation_project.title,
            description=student_data.graduation_project.description,
            student_id=student_obj.id,  # Set the foreign key
        )
        session.add(gp_obj)
        session.commit()
        session.refresh(gp_obj)  # Refresh to get the updated student object
        print("============ gp_obj = ", gp_obj)

    print("============ student_obj = ", student_obj)

    return student_obj


# print("============= Every thing's good ================")