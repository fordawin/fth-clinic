from fastapi import Cookie, HTTPException, Depends
from jose import jwt, JWTError

secret = 'a very shady secret'

def get_token(token: str = Cookie('token')):
    try:
        user = jwt.decode(token, secret)
        if user:
            return user
    except JWTError:
        raise HTTPException(401, 'Please Log In first')

def check_employee(payload: dict = Depends(get_token)):
    role = payload.get("type")
    
    if role != "Employee":
        raise HTTPException(401, 'You are not an Employee.')
    else:
        return payload

def check_admin(payload: dict = Depends(get_token)):
    role = payload.get("type")
    
    if role != "Admin":
        raise HTTPException(401, 'You are not an Admin.')
    else:
        return payload

def check_doctor(payload: dict = Depends(get_token)):
    role = payload.get("type")
    
    if role != "Doctor":
        raise HTTPException(401, 'You are not an Doctor.')
    else:
        return payload

