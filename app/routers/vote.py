from fastapi import APIRouter, status, HTTPException, Depends
from .. import schemas, database, oauth2, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= '/votes',
    tags= ['VOTE']
)

@router.post('/', status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # first checking if the post with passed id exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id: {vote.post_id} does not exist")
    
    # second checking if the vote exists
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    # vote direction
    if vote.vote_dir == 1: # for creating vote
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, 
                                detail= f"the user {current_user.id} has already voted on the post!")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
        
    else: # for deleting vote
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                detail= f"the user {current_user.id} has not voted on this post!")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully delete vote"}