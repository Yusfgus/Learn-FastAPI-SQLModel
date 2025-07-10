from sqlmodel import create_engine, SQLModel, Session
from models import Student, GP

# Database URL
DATABASE_URL = "sqlite:///./students.db"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Function to create the database tables
def init_db():
    SQLModel.metadata.create_all(engine)

def get_student():
    """Get a student by ID."""
    student_id: int = int(input("Enter student ID: "))
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} not found.")
        else:
            print("Student found: ", student)
            if student.gp_rl:
                print("Graduation Project:", student.gp_rl)
            else:
                print("No Graduation Project assigned.")
    

if __name__ == "__main__":
    print("run db.py")
    # Initialize the database when running this script directly
    # init_db()
    get_student()

# Function to get a session for database operations
def get_session():
    """Get a session for database operations."""
    with Session(engine) as session:
        yield session
