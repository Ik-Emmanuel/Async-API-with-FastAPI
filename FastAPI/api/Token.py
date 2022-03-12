from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
import json
from .schemas import TokenData

with open ('vars.json', 'r') as variables:
    env_vars = json.loads(variables.read())  

SECRET_KEY = env_vars['SECRET_KEY']
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #enter the route where token is obtained 



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


#### to be added to every route in order to protect it 
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

