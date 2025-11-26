from pydantic import BaseModel
from typing import TypeVar, Literal, Optional

T = TypeVar["T"]

class ApiResponse(BaseModel):
    status: Literal["success", "failed"]
    status_code: int
    message: str
    data: Optional[T] =  None

    class Config:
        from_attributes = True