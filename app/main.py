from fastapi import FastAPI

from app.schemas import student_schema, subject_schema, GP_schema, email_schema

subject_schema.rebuild_models()
GP_schema.rebuild_models()
email_schema.rebuild_models()

from app.core.database import init_db
from app.routers import GP_router, email_router, student_router, auth, subject_router



# Initialize the database
if __name__ == "__main__":
    print("run main.py")
    # Initialize the database when running this script directly
    # drop_table(table=Email)
    # init_db()


# # Create FastAPI app instance
app = FastAPI()
app.include_router(student_router.router)
app.include_router(subject_router.router)
app.include_router(email_router.router)
app.include_router(GP_router.router)
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