from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from api.config.resources import AUTH_SECRET, AUTH_ALGORITHM, SESSION_LIFETIME, SESSION_MAX_LIFETIME
from api.services.helpers import abort


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def encode_token(username, type):
        payload = dict(iss=username, sub=type)
        to_encode = payload.copy()
        if type == "access_token":
            to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=SESSION_LIFETIME)})
        else:
            to_encode.update({"exp": datetime.utcnow() + timedelta(hours=SESSION_MAX_LIFETIME)})
        return jwt.encode(to_encode, AUTH_SECRET, algorithm=AUTH_ALGORITHM)

    def encode_login_token(self, username):
        access_token = self.encode_token(username, "access_token")
        refresh_token = self.encode_token(username, "refresh_token")

        login_token = dict(
            access_token=f"{access_token}",
            refresh_token=f"{refresh_token}"
        )
        return login_token

    def encode_update_token(self, username):
        access_token = self.encode_token(username, "access_token")
        update_token = dict(access_token=f"{access_token}")
        return update_token

    @staticmethod
    def decode_access_token(token):
        try:
            payload = jwt.decode(token, AUTH_SECRET, algorithms=[AUTH_ALGORITHM])
            if payload['sub'] != "access_token":
                abort('Invalid token')
            return payload['iss']
        except ExpiredSignatureError:
            abort('Signature has expired')
        except JWTError as e:
            abort('Invalid token')

    @staticmethod
    def decode_refresh_token(token):
        try:
            payload = jwt.decode(token, AUTH_SECRET, algorithms=[AUTH_ALGORITHM])
            if payload['sub'] != "refresh_token":
                abort('Invalid token')
            return payload['iss']
        except ExpiredSignatureError:
            abort('Signature has expired')
        except JWTError as e:
            abort('Invalid token')

    def auth_access_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_access_token(auth.credentials)

    def auth_refresh_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_refresh_token(auth.credentials)

    async def verify_token(self, request: Request):
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
            
            token = auth_header.split(" ")[1]
            return self.decode_access_token(token)
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))
