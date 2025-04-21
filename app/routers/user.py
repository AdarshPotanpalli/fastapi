from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix = "/users",
    tags= ['Users']
)

# Create a new user
@router.post('/', response_model = schemas.UserOut, status_code= status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hashing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code= status.HTTP_409_CONFLICT)
    
    new_user = models.User(**user.dict()) # creating a new user 
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # commiting changes to database
    
    return new_user

# Get user bby id, a person can browse the other users
@router.get('/{id}', response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"The user with id: {id} does not exist")
    
    return user