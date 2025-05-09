
# encryption/hashing code
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") # setting the default hashing algorithm (bcrypt)

def hash(password:str):
    return pwd_context.hash(password)

def verify(raw_password: str, hashed_password: str):
    return pwd_context.verify(raw_password, hashed_password)