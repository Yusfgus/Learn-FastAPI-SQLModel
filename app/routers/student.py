from typing import Annotated
from fastapi import Body, Depends, Path, Query, APIRouter, HTTPException
from sqlmodel import Session, select

from ..HelperFunctions import hash_password, verify_password
from ..db import get_session
from ..dependencies import CommonQueryParams
from ..models.student_model import Department, Student, StudentCreate, StudentPublic, StudentPublicWithAll, StudentPublicWithGP, StudentUpdate
from ..models.subject_model import Subject, SubjectPublic
from ..models.email_model import Email, EmailCreate, EmailPublicWithAll
from ..models.GP_model import GP


router = APIRouter(
    prefix="/students",
    tags=["students"],
)


# Endpoint to get all students or filter by department or age or id
@router.get("/", response_model=list[StudentPublic])
def get_students(
    commons: Annotated[CommonQueryParams, Depends()],
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
@router.get("/{student_id}", response_model=StudentPublicWithAll)
def get_student_by_id(
    student_id: Annotated[int, Path(title="Student ID")],
    session: Session = Depends(get_session),
) -> Student:
    
    student = session.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    return student


@router.post("/add", response_model=StudentPublicWithGP)
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
@router.patch("/{student_id}", response_model=StudentPublic)
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
@router.delete("/{student_id}", response_model=dict[str, str | StudentPublic])
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


# Endpoint for logging in a student
@router.post("/login")
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


# assign email to a student
@router.post("/{student_id}/emails/add", response_model=EmailPublicWithAll)
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


# get a student subjects
@router.get("/{student_id}/subjects", response_model=list[SubjectPublic])
def get_student_subjects(
    student_id: Annotated[int, Path(title="Student ID")],
    session: Session = Depends(get_session),
) -> list[Subject]:
    
    student = session.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    return student.subjects


# assign subject to a student
@router.post("/{student_id}/subjects")
def add_subject_to_student(
    student_id: Annotated[int, Path(title="Student ID")],
    subject_ids: Annotated[list[int], Body(title="Subjects IDs")],
    session: Session = Depends(get_session),
) -> dict:
    
    student = session.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="student not found")

    subjects_names = []
    for subject_id in subject_ids:
        subject = session.get(Subject, subject_id)
        if subject is None:
            raise HTTPException(status_code=404, detail="subject not found")

        # Check if the subject is already added to the student
        if subject in student.subjects:
            raise HTTPException(status_code=400, detail="Subject already added to student")
        
        student.subjects.append(subject)
        session.add(student)
        session.commit()
        subjects_names.append(subject.name)

    return {
        "message": f"Subject \'{subjects_names}\' added to student \'{student.name}\' successfully"
    }
