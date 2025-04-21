from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix= "/posts",
    tags = ['Posts'] # for grouping in SwaggerUI documentation
)


@router.get('/', response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip : int = 0, search : Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""") # execute any SQL query
    # posts = cursor.fetchall() # this is the way to fetch any post
    
    # limit gives the number of queries
    # skip gives offset, used for pagination
    # search gives search keyword
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # get number of votes for all the posts using SQL LEFT OUTER JOIN
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter= True).group_by(models.Post.id). \
        filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.post('/', status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    # #we use docstring with place holders to avoid SQL injections
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", # place holders
    #                (post.title, post.content, post.published)) # values
    # new_post = cursor.fetchone()
    # conn.commit() # we need to commit the staged changes to observe any difference in database

    new_post = models.Post(owner_id = current_user.id, **post.dict()) # we dont need to manually map each table element to pydantic schema
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # similar to RETURNING *
    
    return new_post # usually when we create a post request, the return should show the new element created
    

#getting a specific post via path parameter
@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) # converting to string is important
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first() # filtering the post, if we dont use first() it will just be a raw query
        
    # get number of votes for the requested post using SQL LEFT OUTER JOIN
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter= True).group_by(models.Post.id). \
        filter(models.Post.id == id).first()    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"The post with id: {id} not found")
    return post



# deleting a post
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT) # default status code for delete
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone() # deleted post
    # conn.commit() # commit the changes
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post!")
    
    post_query.delete(synchronize_session= False) # dont exactly know the meaning of this argument
    db.commit()

    # return response
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, post : schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # always specify pydantic schema for update and post + type of id for better validation
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    
    if updated_post ==  None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this post!")
    
    post_query.update(post.dict(), synchronize_session= False) # payload -> pydantic schema -> dict
    db.commit() 
    
    return post_query.first()