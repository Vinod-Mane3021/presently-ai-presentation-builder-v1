from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.user import UserOut, UserSignin, UserCreate
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# create user api
@router.post("/sign-in", response_model=UserOut, status_code=status.HTTP_200_OK)
def signin_user(request: UserSignin, db: Session=Depends(get_db)):
    try:
        user = UserService.signin_user(db, email=request.email, raw_password=request.password)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/sign-up", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup_user(request: UserCreate, db: Session=Depends(get_db)):
    try:
        user = UserService.signup_user(db, request)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))