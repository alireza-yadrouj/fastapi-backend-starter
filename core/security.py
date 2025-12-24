from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "mysecretkey123"         #  در پروژه واقعی طولانی و امن باشد
ALGORITHM = "HS256"                   # الگوریتم امضا
ACCESS_TOKEN_EXPIRE_MINUTES = 30      # اعتبار توکن به دقیقه


def hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password is too long (max 72 bytes)")
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
