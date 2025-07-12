from sqlmodel import create_engine, SQLModel, Session

# sqlite_url = "sqlite:///./students.db"
# Create the database engine
# connect_args = {"check_same_thread": False} # make sure we don't share the same session in more than one request
# engine = create_engine(sqlite_url, echo=True, connect_args=connect_args) # remove echo=True in production


#  DATABASE_URL = "mysql+pymysql://<username>:<password>@<host>/<database>"
DATABASE_URL = "mysql+pymysql://root:manga123@localhost/college"
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
