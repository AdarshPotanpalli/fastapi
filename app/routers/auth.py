# contains the route for authentication
from fastapi import HTTPException, APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, models, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags = ['Authentication']
)

@router.post("/login", response_model= schemas.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= "Invalid creadentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail = "Invalid credentials")
        
    jwt_token = oauth2.create_jwt_token(data = {"user_id": user.id}) # gets the authentication token
        
    return {"access_token": jwt_token, "token_type": "bearer"} # a token needs to be returned if credentials are correct