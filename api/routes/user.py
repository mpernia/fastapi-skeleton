from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.config.database as _database
import api.services.user as _users
import api.schemas.user as _schemas
import api.middlewares.authenticate as _auth
from api.services.helpers import abort

auth_handler = _auth.AuthHandler()

conn_db = Depends(_database.get_db)

router = APIRouter()


@router.post("/register", status_code=201, response_model=_schemas.User, tags=["Users"])
def create_user(user: _schemas.UserCreate, db: Session = conn_db):
    db_user = _users.get_user_by_username(db=db, username=user.username)
    if db_user:
        abort('The E-Mail is already used')
    user.password = auth_handler.get_password_hash(user.password)
    return _users.create_user(db=db, user=user)


@router.post("/login", response_model=_schemas.LoginToken, tags=["Users"])
def login_user(user: _schemas.UserCreate, db: Session = conn_db):
    db_user = _users.get_user_by_username(db=db, username=user.username)
    if db_user is None:
        abort('The E-Mail is not exist')
    is_verified = auth_handler.verify_password(user.password, db_user.hashed_password)
    if not is_verified:
        abort('Password does not matched')
    return auth_handler.encode_login_token(user.username)


@router.get("/users", response_model=List[_schemas.User], tags=["Users"])
def read_user(skip: int = 0, limit: int = 10, db: Session = conn_db,
              username=Depends(auth_handler.auth_access_wrapper)):
    if username is None:
        abort()
    db_users = _users.get_users(db=db, skip=skip, limit=limit)
    return db_users


@router.get("/update_token", response_model=_schemas.UpdateToken, tags=["Users"])
def update_token(username=Depends(auth_handler.auth_refresh_wrapper)):
    if username is None:
        abort()
    return auth_handler.encode_login_token(username)

