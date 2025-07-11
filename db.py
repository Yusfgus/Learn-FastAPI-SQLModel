from sqlmodel import create_engine, SQLModel, Session

# Database URL
DATABASE_URL = "sqlite:///./students.db"


# Create the database engine
engine = create_engine(DATABASE_URL, echo=True) # remove echo=True in production


# Function to create the database tables
def init_db():
    print("Initializing the database...")
    SQLModel.metadata.create_all(engine)


# Function to get a session for database operations
def get_session():
    """Get a session for database operations."""
    with Session(engine) as session:
        yield session
    

def drop_table(table: SQLModel):
    """Drop the Email table if it exists."""
    SQLModel.metadata.drop_all(engine, tables=[table.__table__])
