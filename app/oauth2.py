from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, models
from .database import get_db
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRE_TIME = settings.access_token_expire_minutes

# Creation of token
def create_jwt_token(data: dict):
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= EXPIRE_TIME)
    to_encode.update({"exp": expire}) # adding the expiration time
    
    encoded_jwt_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    
    return encoded_jwt_token

# Verification of Token
def verify_jwt_token(token: str, credential_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM]) # decoding the payload
        id: str = payload.get("user_id") # getting the user id from payload
        
        if id is None:
            raise credential_exception
        
        token_data = schemas.TokenData(id = str(id))
    
    except JWTError:
        raise credential_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    credential_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                                         detail= "Couldn't validate the credentials", headers= {"WWW-Authenticate": "Bearer"})
    
    token = verify_jwt_token(token, credential_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first() # returning the user, this is what this function is for
    
    return user
    