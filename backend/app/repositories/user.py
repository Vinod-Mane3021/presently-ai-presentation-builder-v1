from sqlalchemy.orm import Session
from app.models.user import User
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from typing import Optional, Iterable


class UserRepo:
    @staticmethod
    def create(
        db: Session,
        *,
        email: str,
        full_name: str,
        hashed_password: str,
        providers: list[str] | None = None,
        picture_url: str | None = None,
        user_metadata: dict | None = None,
        created_by: UUID | None = None,
    ) -> User:
        user = User(
            email=email,
            full_name=full_name,
            password=hashed_password,
            providers=providers,
            picture_url=picture_url,
            user_metadata=user_metadata,
            created_by=created_by,
        )
        try:
            db.add(user)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("email already exist")
        db.refresh(user)
        return user

    @staticmethod
    def get(db: Session, user_id: UUID) -> Optional[User]:
        return db.get(User, user_id)

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> Iterable[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update(
        db: Session,
        user: User,
        *,
        email: str | None = None,
        full_name: str | None = None,
        hashed_password: str | None = None,
        providers: list[str] | None = None,
        picture_url: str | None = None,
        user_metadata: dict | None = None,
        last_signin_at=None,
        updated_by=None,
    ) -> User:
        if email is not None:
            user.email = email
        if full_name is not None:
            user.full_name = full_name
        if hashed_password is not None:
            user.password = hashed_password
        if providers is not None:
            user.providers = providers
        if picture_url is not None:
            user.picture_url = picture_url
        if user_metadata is not None:
            user.user_metadata = user_metadata
        if last_signin_at is not None:
            user.last_signin_at = last_signin_at
        if updated_by is not None:
            user.updated_by = updated_by
        db.add(user)
        db.commit(user)
        db.refresh(user)
        return user
