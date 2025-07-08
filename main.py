from fastapi import FastAPI, HTTPException, Query, Path
from typing import Annotated
from models import *
from contextlib import asynccontextmanager
from db import init_db

# Initialize the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database
    init_db()
    yield
    # Here you can add any cleanup code if needed

# Create FastAPI app instance
app = FastAPI(lifespan=lifespan)


# # Root endpoint
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# # About endpoint
# @app.get("/about")
# def about() -> str:
#     return "This is the about page"


# # Add 50 to a given number via query parameter
# @app.get("/add 50")
# def add_50(num: int) -> int:
#     return num + 50


# # List of student dictionaries with id, name, age, and job
# student_list = [
#     {"id": 1, "name": "Alice", "age": 20, "department": 'cs', "subjects": [Subject(name="Math", hours=3), Subject(name="Physics", hours=4)]},
#     {"id": 2, "name": "Bob", "age": 22, "department": "IS"},
#     {"id": 3, "name": "Charlie", "age": 23, "department": "sc", "subjects": [{"name": "Chemistry", "hours": 3},]},
#     {"id": 4, "name": "David", "age": 21, "department": "cs"},
#     {"id": 5, "name": "Eve", "age": 22, "department": 'Csys'},
# ]


# # Endpoint to get all students or filter by department or age or id
# @app.get("/students")
# def get_students(
#     id: Annotated[int | None, Query(gt=0)] = None,
#     department: Department | None = None,
#     age: Annotated[int | None, Query(gt=0, le=100)] = None,
#     limit: Annotated[int | None, Query(gt=0)] = None,
#     skip: Annotated[int | None, Query(gt=0)] = None,
#     ) -> list[StudentWithID]:
    
#     filtered_students = [StudentWithID(**s) for s in student_list]

#     if id is not None:
#         # If id is provided, filter the student list
#         filtered_students = [s for s in filtered_students if s.id == id]

#     if department is not None:
#         # If department is provided, filter the student list
#         filtered_students = [s for s in filtered_students if s.department.lower() == department.value]

#     if age is not None:
#         # If age is provided, filter the student list
#         filtered_students = [s for s in filtered_students if s.age == age]

#     if skip is not None:
#         # If skip is provided, apply the skip to the student list
#         filtered_students = filtered_students[skip:]

#     if limit is not None:
#         # If limit is provided, apply the limit to the student list
#         filtered_students = filtered_students[:limit]

#     return filtered_students


# # Endpoint to get a single student by id
# @app.get("/students/{student_id}")
# def get_student_by_id(student_id: Annotated[int, Path(title="Student ID")]) -> StudentWithID:
#     for student in student_list:
#         if student["id"] == student_id:
#             return StudentWithID(**student)
#     raise HTTPException(status_code=404, detail="student not found")


# # Endpoint to get students by department type
# @app.get("/departments")
# def get_all_department() -> list[str]:
#     return Department.__members__.keys()


# @app.post("/students/add")
# def add_student(new_student: StudentCreate) -> StudentWithID:
#     id = len(student_list) + 1
#     student = StudentWithID(id=id, **new_student.model_dump()).model_dump()
#     student_list.append(student)
#     return student


# print("============= Every thing's good ================")