from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from draft_tracker_system.utils.config import build_db_url
from draft_tracker_system.db.session import get_engine, get_api_session
from draft_tracker_system.db.models import User

from draft_tracker_system.services.user_service import register_player, login_user, change_password, delete_user
from draft_tracker_system.utils.security import create_access_token, decode_token

security = HTTPBearer()
router = APIRouter()

engine = get_engine(build_db_url())
SessionLocal = get_api_session(engine)


def get_db(session_factory):
    def _get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()
    return _get_db


get_session = get_db(SessionLocal)

@router.post("/register")
def register(
    username: str,
    password: str,
    session: Session = Depends(get_session)
):
    user = register_player(session, username, password)
    return {
        "message": "User created",
        "user_id": user.user_id
    }

@router.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_session)
):
    user = login_user(db, username, password)

    token = create_access_token({
        "user_id": user.user_id,
        "role": user.role.role_name
    })

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role.role_name
    }

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session)
):
    token = credentials.credentials  # auto extracted by FastAPI

    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")

    user = db.query(User).filter_by(user_id=user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

@router.put("/change-password")
def update_password(
    target_user_id: int,
    old_password: str = None,
    new_password: str = None,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    user = change_password(
        db,
        current_user,
        target_user_id,
        old_password,
        new_password
    )

    return {
        "message": "Password updated successfully",
        "user_id": user.user_id
    }

@router.delete("/user/{user_id}")
def remove_user(
    user_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    result = delete_user(db, current_user, user_id)

    return {
        "message": "User deleted successfully",
        "data": result
    }