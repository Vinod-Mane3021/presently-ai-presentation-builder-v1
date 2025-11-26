from app.repositories.user import UserRepo
from app.lib.password import verify_password, hash_password
from app.schemas.user import UserOut, UserSignin, UserCreate, UserUpdate
from uuid import UUID


class UserService:
    @staticmethod
    def signin_user(db, email, raw_password):
        existing_user = UserRepo.get_by_email(db, email)
        if existing_user is None:
            raise ValueError("user not found")
        hashed = verify_password(raw_password, existing_user.password)
        if hashed:
            return existing_user
        else:
            raise ValueError("invalid password")

    @staticmethod
    def signup_user(db, request: UserCreate):
        if UserRepo.get_by_email(db, request.email):
            raise ValueError("email already exist")
        hashed = hash_password(request.password)
        print("hashed", hashed)
        return UserRepo.create(
            db,
            email=request.email,
            full_name=request.full_name,
            hashed_password=hashed,
            providers=request.providers,
            picture_url=request.picture_url,
            user_metadata=request.user_metadata,
            created_by=request.created_by,
        )

    @staticmethod
    def update_user(db, user_id: UUID, request: UserUpdate):
        user = UserRepo.get(db, user_id)
        if user is None:
            raise ValueError("user not found")
        return UserRepo.update(
            db,
            user,
            email=request.email,
            full_name=request.full_name,
            providers=request.providers,
            picture_url=request.picture_url,
            user_metadata=request.user_metadata,
            last_signin_at=request.last_signin_at,
            updated_by=request.updated_by,
        )