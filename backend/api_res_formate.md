Perfect — your folder layout is already clean, so here’s exactly **where each file should go** for the response-wrapping system we built:

---

### ✅ 1. Common Response Model

**File:** `app/schemas/common.py`
**Purpose:** Define the generic `ApiResponse` class.

```python
# app/schemas/common.py
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel
from typing_extensions import Literal

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status: Literal["success", "error"]
    status_code: int
    message: str
    data: Optional[T] = None

    class Config:
        from_attributes = True
```

---

### ✅ 2. Response Utility Helpers

**File:** `app/lib/responses.py` (recommended new small util file)

If you don’t have a `lib` folder (you do!), that’s the right place for these helpers — keeps routers/services clean.

```python
# app/lib/responses.py
from typing import Any
from app.schemas.common import ApiResponse

def ok(data: Any = None, message: str = "OK", status_code: int = 200):
    return ApiResponse(status="success", status_code=status_code, message=message, data=data)

def created(data: Any = None, message: str = "Created"):
    return ApiResponse(status="success", status_code=201, message=message, data=data)

def fail(message: str, status_code: int):
    return ApiResponse(status="error", status_code=status_code, message=message, data=None)
```

---

### ✅ 3. Exception Handlers (Global)

**File:** `app/main.py`
Add these below your FastAPI app creation:

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from app.schemas.common import ApiResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(
            status="error",
            status_code=exc.status_code,
            message=str(exc.detail),
            data=None,
        ).model_dump(),
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=ApiResponse(
            status="error",
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation error",
            data=exc.errors(),
        ).model_dump(),
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=ApiResponse(
            status="error",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            data=None,
        ).model_dump(),
    )
```

---

### ✅ 4. Update Your User Router

**File:** `app/routers/user.py`

Use the helpers and response model consistently:

```python
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.user import UserService
from app.schemas.user import UserOut, UserSignin, UserCreate
from app.schemas.common import ApiResponse
from app.lib.responses import ok, created

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/sign-in", response_model=ApiResponse[UserOut], status_code=status.HTTP_200_OK)
def signin_user(request: UserSignin, db: Session = Depends(get_db)):
    try:
        user = UserService.signin_user(db, email=request.email, raw_password=request.password)
        return ok(user, message="Signed in successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/sign-up", response_model=ApiResponse[UserOut], status_code=status.HTTP_201_CREATED)
def signup_user(request: UserCreate, db: Session = Depends(get_db)):
    try:
        user = UserService.signup_user(db, request)
        return created(user, message="User created successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
```

---

### 📂 Final Folder Summary

```
app/
├── lib/
│   ├── responses.py              ✅ new helper
│
├── routers/
│   ├── user.py                   ✅ use ok() / created()
│
├── schemas/
│   ├── common.py                 ✅ ApiResponse model
│   ├── user.py
│
├── services/
│   ├── user.py
│
├── main.py                       ✅ exception handlers
```

---

This keeps your API consistent and clean — every route now returns:

```json
{
  "status": "success",
  "status_code": 200,
  "message": "Signed in successfully",
  "data": { "id": "...", "email": "..." }
}
```

Would you like me to include a shared error response (e.g. `ErrorResponse` schema) for Swagger docs auto-generation too?
