from datetime import timedelta, datetime
import jwt
from django.conf import settings

def create_token(userId: int) -> dict:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        'user_id': userId,
        'access_token': create_access_token(
            data={'user_id': userId}, expires_delta=access_token_expires    
        ),
        'token_type': 'Token'
    }

def create_access_token(data:dict, expires_delta:timedelta = 15):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire, 'sub': 'access'})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt
    
    
    