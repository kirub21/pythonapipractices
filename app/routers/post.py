from typing import List, Optional
from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, oauth2,schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)



@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    get_current_user: dict = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 2,
    search: Optional[str] = ""
):  
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()
    
    try:
        results = (
            db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
            .group_by(models.Post.id).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()
        )
        
        # Convert results to a list of dictionaries
        return [{"post": post, "votes": votes} for post, votes in results]
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"An error occurred: {error}")


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    get_current_user: dict = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} not found"
        )
    if post.owner_id != get_current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to access this resource"
        )
    return post.__dict__


@router.delete("/{id}")
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    get_current_user: dict = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} not found"
        )
    if post.owner_id != get_current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to delete this post"
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(
    id: int,
    post: dict,
    db: Session = Depends(get_db),
    get_current_user: dict = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} not found"
        )
    if existing_post.owner_id != get_current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to update this post"
        )
    post_query.update(post, synchronize_session=False)
    db.commit()
    return post_query.first().__dict__
