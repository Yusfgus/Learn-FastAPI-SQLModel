from fastapi import FastAPI
from .db import init_db
from .routers import student, subject, email, GP
from .HelperFunctions import rebuld_models


# Initialize the database
if __name__ == "__main__":
    print("run main.py")
    # Initialize the database when running this script directly
    # drop_table(table=Email)
    init_db()


# # Create FastAPI app instance
app = FastAPI()
app.include_router(student.router)
app.include_router(subject.router)
app.include_router(email.router)
app.include_router(GP.router)


@app.on_event("startup")
def on_startup():
    print("Starting up the FastAPI application...")
    rebuld_models()


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


# # Endpoint to get students by department type
# @app.get("/departments")
# def get_all_department() -> list[str]:
#     return Department.__members__.keys()


print("============= Every thing's good ================")