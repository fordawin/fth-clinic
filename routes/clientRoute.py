from fastapi import FastAPI, APIRouter, Depends, HTTPException, Cookie, status, Response, Request
from sqlalchemy.orm import Session
from dotenv import dotenv_values
from schemas.userCredentialSchema import LoginForm, TokenData
from models.userCredentialModel import User_credential
from schemas.clientSchema import clientUpdate
from models.clientModel import Client
from models.doctorModel import Doctor
from models.employeeModel import Employee
from database import get_db
from dependencies import get_token
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
import time

#image upload
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image
import secrets

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# app = FastAPI()
config_credentials = dict(dotenv_values(".env"))

secret = config_credentials["SECRET"]
def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)

router = APIRouter(
    prefix='/client',
    tags=['client']
)

templates = Jinja2Templates(directory="templates")

# app.mount("/../static", StaticFiles(directory="static"), name="static")
# @router.get("/")
# def registration(request: Request):
#     return templates.TemplateResponse("clientside/home.html", {"request": request})

# @router.get("/login")
# def registration(request: Request):
#     return templates.TemplateResponse("clientside/login.html", {"request": request})

# @router.post('/login')
# async def verify(response: Response, request: Request, form_data: LoginForm = Depends(LoginForm.as_form), db: Session = Depends(get_db)):

#     # email = user.user_email
#     # password = form.get("password")
#     try:
#         user = db.query(User_credential).filter(User_credential.user_email == form_data.user_email).first()
#         if user:
#             match = password_verify(form_data.user_password, user.user_password)
#             if match:
#                 data = TokenData(email = user.user_email, type = user.user_type)
#                 token = jwt.encode(dict(data), secret)
#                 response.set_cookie('token', token, httponly=True)
#                 return templates.TemplateResponse("clientside/home.html", {"request": request})
#     except Exception as e:
#         print(e)

@router.get('/uploadProfile/{id}', status_code=status.HTTP_202_ACCEPTED)
async def upload_profile(id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    verify = db.query(Client).filter(Client.cl_id == id).first()

    FILEPATH = "static/images/"
    filename = file.filename
    extension = filename.split(".")[1]

    if extension not in ["png", "jpg"]:
        return {"status" : "Error", "detail": "Image Extension Not Allowed!"}
    
    token_name = secrets.token_hex(10)+"."+extension
    generate_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generate_name, "wb") as file:
        file.write(file_content)
    
    #pillow
    img = Image.open(generate_name)
    img = img.resize(size = (200, 200))
    img.save(generate_name)

    file.close()

    verify.cl_pic = token_name
    db.add(verify)
    db.commit()

    file_url = "localhost:8000" + generate_name[1:]
    return {"status": "ok", "filename": file_url}


@router.get('/')
def findAll(db: Session = Depends(get_db)):
    users = db.query(Client).filter(Client.cl_status == "Active").all()

    return {'users': users}

@router.get('/{id}', status_code=status.HTTP_202_ACCEPTED)
def findOne(id: str, db: Session = Depends(get_db)):

    user = db.query(Client).filter(Client.cl_id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'CLient does not exists')

    return {'user': user}

# @router.post('/admin/{id}', response_model=clientUpdate)
# def update(id: str, form_data: clientUpdate, db: Session = Depends(get_db)):
#     verify = db.query(Client).filter(Client.cl_id == id).first()
#     user_num_cl = db.query(Client).filter(Client.cl_contactNo == form_data.cl_contactNo).first()
#     user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == form_data.cl_contactNo).first()
#     user_num_em = db.query(Employee).filter(Employee.em_contactNo == form_data.cl_contactNo).first()

#     if not verify:
#         raise HTTPException(404, 'User to update is not found')

#     listss = [form_data.cl_firstName, " ", form_data.cl_middleName, " ", form_data.cl_lastName]
    
#     form_data.cl_fullName = f"{form_data.cl_firstName}{form_data.cl_middleName}{form_data.cl_lastName}"
#     form_data.cl_address = f"{form_data.cl_houseNo}{form_data.cl_street}{form_data.cl_brgy}{form_data.cl_brgy}"
    
#     # print (form_data.cl_fullName)
    
#     if form_data.cl_contactNo == verify.cl_contactNo:
#         user_data = form_data.dict(exclude_unset=True)
#         for key, value in user_data.items():
#             setattr(verify, key, value)
#             # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
#         db.add(verify)
#         db.commit()
        
#     else:
#         if not user_num_cl: 
#             if not user_num_doc: 
#                 if not user_num_em:
#                         user_data = form_data.dict(exclude_unset=True)
#                         for key, value in user_data.items():
#                             setattr(verify, key, value)
#                             # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
#                         db.add(verify)
#                         db.commit()

#                 else:
#                     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')
#             else:
#                 raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')
#         else:
#             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')

#     # time.sleep(1)

#     # response = RedirectResponse(url='/users/profile', status_code=302)

#     return

@router.post('/admin/{id}', response_model=clientUpdate)
async def update(id: str, form_data: clientUpdate, db: Session = Depends(get_db)):
    verify = db.query(Client).filter(Client.cl_id == id).first()
    user_num_cl = db.query(Client).filter(Client.cl_contactNo == form_data.cl_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == form_data.cl_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == form_data.cl_contactNo).first()

    if not verify:
        raise HTTPException(404, 'User to update is not found')
    
    # if form_data.cl_contactNo == verify.cl_contactNo:
    #     user_data = form_data.dict(exclude_unset=True)
    #     for key, value in user_data.items():
    #         setattr(verify, key, value)
    #         # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
    #     db.add(verify)
    #     db.commit()
        
    #     return
        
    # else:
    if not user_num_cl: 
        if not user_num_doc: 
            if not user_num_em:
                user_data = form_data.dict(exclude_unset=True)
                for key, value in user_data.items():
                    setattr(verify, key, value)
                        # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
                db.add(verify)
                db.commit()

                return
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')

    # time.sleep(1)

    # response = RedirectResponse(url='/admin/client', status_code=302)

    return response
  
@router.get('/deactivate/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not cancel:
        raise HTTPException(404, 'User to cancel is not found')
    else:
        db.query(User_credential).filter(User_credential.user_id == id).update({'user_status': "Inactive"})
        
    db.commit()

    time.sleep(1)  
    response = RedirectResponse(url='/admin/client/', status_code=302)
    return response
