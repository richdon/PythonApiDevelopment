from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import models, schemes, oauth2, database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def voting(vote: schemes.Vote, db: Session = Depends(database.get_db),
           current_user=Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {vote.post_id} does not exist')

    # checks if the user already voted for this specific post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has'
                                                                             f' already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'successfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='vote does not exist')
        vote_query.delete()
        db.commit()
        return {'message': 'successfully deleted vote'}
