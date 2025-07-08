from sqlmodel import create_engine, SQLModel, Session

# Database URL
DATABASE_URL = "sqlite:///./students.db"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Function to create the database tables
def init_db():
    SQLModel.metadata.create_all(engine)


