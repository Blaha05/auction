from fastapi import Depends, HTTPException
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class Token:

    def create_token(self, data:dict, key:str, time:int):
        expire = datetime.utcnow() + timedelta(minutes=time)
        data.update({'exp': expire})
        token = jwt.encode(data, key)
        return token


    def decode_token(self, token, key):
        try:
            decode = jwt.decode(token, key, 'HS256')
            return decode
        except:
            return 'Token is not valide'
        

from fastapi import Depends, HTTPException, Cookie, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    request: Request = None,  # Для отримання cookies
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        token = request.cookies.get("access_token")
        print(token)
        if not token:
            raise credentials_exception
        
    try:
        payload = jwt.decode(token, 'Secret', algorithms=['HS256'])
        return payload  # Поверніть дані токена, наприклад, user ID чи email
    except jwt.JWTError:
        raise credentials_exception

    

