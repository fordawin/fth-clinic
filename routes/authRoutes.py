from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
from database import get_db
from models.userCredentialModel import User_credential
from schemas.userCredentialSchema import TokenData, LoginForm
from jose import jwt
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from dotenv import dotenv_values
config_credentials = dict(dotenv_values(".env"))

secret = config_credentials["SECRET"]

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)



router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

templates = Jinja2Templates(directory="templates")

# @router.get("/")
# def registration(request: Request):
#     return templates.TemplateResponse("adminside/admin.html", {"request": request})

@router.get("/")
def registration(request: Request):
    return templates.TemplateResponse("adminside/login.html", {"request": request}) 

@router.post('/')
async def login(response: Response, form_data: LoginForm = Depends(LoginForm.as_form), db: Session = Depends(get_db)):
    try:
        user = db.query(User_credential).filter(User_credential.user_email == form_data.user_email).first()
        if user:
            match = password_verify(form_data.user_password, user.user_password)
            if match:
                data = TokenData(id = user.user_id, email = user.user_email, type = user.user_type)
                token = jwt.encode(dict(data), secret)
                response = RedirectResponse(url='/admin', status_code=302)
                response.set_cookie('token', token, httponly=True)
                return response

    except Exception as e:
        print(e)

@router.get('/logout')
def logout(response: Response):
    response = RedirectResponse(url='/auth', status_code=307)
    response.delete_cookie('token')
    return response