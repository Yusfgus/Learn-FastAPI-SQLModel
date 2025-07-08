from fastapi import FastAPI, HTTPException
from schemas import *


# Create FastAPI app instance
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


# List of student dictionaries with id, name, age, and job
student_list = [
    {"id": 1, "name": "Alice", "age": 20, "departement": 'cs', "subjects": [Subject(name="Math", hours=3), Subject(name="Physics", hours=4)]},
    {"id": 2, "name": "Bob", "age": 22, "departement": "IS"},
    {"id": 3, "name": "Charlie", "age": 23, "departement": "sc"},
    {"id": 4, "name": "David", "age": 21, "departement": "cs"},
    {"id": 5, "name": "Eve", "age": 22, "departement": 'Csys'},
]


# Endpoint to get all students or filter by departement
@app.get("/students")
def get_students(departement: Departement | None = None) -> list[StudentWithID]:
    if departement is not None:
        # If departement is provided, filter the student list
        return [StudentWithID(**student) for student in student_list if student["departement"].lower() == departement.value]
    else:
        # If no departement is provided, return all students
        return [StudentWithID(**student) for student in student_list]


# Endpoint to get a single student by id
@app.get("/students/{student_id}")
def get_student_by_id(student_id: int) -> StudentWithID:
    for student in student_list:
        if student["id"] == student_id:
            return StudentWithID(**student)
    raise HTTPException(status_code=404, detail="student not found")


# Endpoint to get students by departement type
@app.get("/students/departements/{departement_type}")
def get_student_by_job(departement_type: Departement) -> list[StudentWithID]:
    filtered_students = [student for student in student_list if student["departement"].lower() == departement_type.value]
    if not filtered_students:
        raise HTTPException(status_code=404, detail="No students found for this departement type")
    return filtered_students


@app.post("/students/add")
def add_student(new_student: StudentCreate) -> StudentWithID:
    id = len(student_list) + 1
    student = StudentWithID(id=id, **new_student.model_dump()).model_dump()
    student_list.append(student)
    return student


print("Every thing good")