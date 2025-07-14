from fastapi import FastAPI

from app.models import student_model, subject_model, GP_model, email_model

subject_model.rebuild_models()
GP_model.rebuild_models()
email_model.rebuild_models()

from app.db import init_db
from app.routers import student, subject, email, GP, auth



# Initialize the database
if __name__ == "__main__":
    print("run main.py")
    # Initialize the database when running this script directly
    # drop_table(table=Email)
    # init_db()


# # Create FastAPI app instance
app = FastAPI()
app.include_router(student.router)
app.include_router(subject.router)
app.include_router(email.router)
app.include_router(GP.router)
app.include_router(auth.router)


@app.on_event("startup")
def on_startup():
    print("Starting up the FastAPI application...")


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

from typing import Annotated
from fastapi import Header
from pydantic import BaseModel

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


@app.get("/headers")
async def read_headers(headers: Annotated[CommonHeaders, Header()]):
    print(headers)
    return headers




print("============= Every thing's good ================")