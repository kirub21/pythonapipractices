from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])

@router.post('/login',response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    # Validate user by email (username from the form maps to email)
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )

    # Verify password
    if not utils.verify(user_credentials.password, user.Password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )

    # Create access token
    access_token = oauth2.create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
