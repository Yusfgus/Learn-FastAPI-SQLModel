from typing import Annotated
from pydantic import Field

class CommonQueryParams:
    def __init__(
            self, q: str | None = None, 
            skip: Annotated[int, Field(ge=0)] = 0, 
            limit: Annotated[int, Field(gt=0, le=100)] = 100
    ):
        self.q = q
        self.skip = skip
        self.limit = limit