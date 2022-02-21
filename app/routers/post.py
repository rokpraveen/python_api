from sqlalchemy import func
from app import oauth2
from .. import models, schemas, utils, oauth2
from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/get/myposts", response_model=List[schemas.PostResponse])
def my_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    myposts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    
    return myposts


@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
            limit: int = 5, skip: int = 0, search: Optional[str] = ""): # Now adding query parameters to this get request
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    myposts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return myposts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title, post.content,post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostVoteResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts where id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"ERROR": f"ID: {id} is not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # cursor.fetchone()
    # deleted_post = connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    deleted_post = post_query.first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with ID: {id} was not found!!!!!")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You are not authorized to DELETE this post!!!!!")
    
    
    post_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING * """, (post.title, post.content, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    
    posts = updated_post.first()
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with ID: {id} was not found!!!!!")
    
    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You are not authorized to UPDATEf this post!!!!!")
    
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_post.first()


