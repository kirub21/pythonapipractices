
 
 
from .. import models,utils,schemas
from fastapi import FastAPI, HTTPException, Response, status, Depends,APIRouter
from ..database import engine, sessionLocal,get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/users",
    tags=['users']
)
models.Base.metadata.create_all(bind=engine)
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserCreate )
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
     hashed_password = utils.hash(user.Password)
     user.Password = hashed_password
     

     new_user=models.Users(**user.dict())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user 
@router.get('/{id}',response_model=schemas.UserSchema)
def get_user(id:int,db:Session=Depends(get_db)):
     
    user=db.query(models.Users).filter(models.Users.id ==id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id: {id} does not exist")
    return user