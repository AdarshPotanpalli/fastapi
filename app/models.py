from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, unique= True, nullable= False, primary_key= True)
    title = Column(String, nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default='TRUE', nullable= False) # server_default is needed to set the default values
    created_at = Column(TIMESTAMP(timezone= True), server_default= text('now()')) # setting the timestamp
    
    # setting the foreign key
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable= False)
    
    owner = relationship("User") 
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, unique= True, nullable= False, primary_key= True)
    email = Column(String, unique= True, nullable= False)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), server_default= text('now()'))
    
class Vote(Base):
    
    __tablename__ = "votes"
    
    post_id = Column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), primary_key= True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), primary_key= True)