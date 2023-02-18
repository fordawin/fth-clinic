from fastapi import APIRouter, Depends, HTTPException, Cookie, status, Response, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
from schemas.employeeSchema import employeeUpdate
from schemas.paymentSchema import PaymentBase, PaymentUpdate
from schemas.userCredentialSchema import UserBase, EmployeeBase
from models.userCredentialModel import User_credential
from models.clientModel import Client
from models.paymentModel import Payment
from models.doctorModel import Doctor
from models.employeeModel import Employee
from models.ordersModel import Orders
from database import get_db
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import time
from jose import jwt
from for_email import *
from datatables import DataTable
from dependencies import get_token, check_employee

#image upload
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image
import secrets


from dotenv import dotenv_values
config_credentials = dict(dotenv_values(".env"))

secret = config_credentials["SECRET"]

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)

router = APIRouter(
    prefix='/employee',
    tags=['employee'], dependencies=[Depends(check_employee)]
)

templates = Jinja2Templates(directory="templates")

@router.post('/{id}')
def update(id: str, user: employeeUpdate, db: Session = Depends(get_db)):
    verify = db.query(Employee).filter(Employee.em_id == id).first()
    user_num_cl = db.query(Client).filter(Client.cl_contactNo == user.em_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == user.em_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == user.em_contactNo).first()

    if not verify:
        raise HTTPException(404, 'User to update is not found')

    if user.em_contactNo == verify.em_contactNo:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
            # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
        db.add(verify)
        db.commit()
    else:
        if not user_num_cl: 
            if not user_num_doc: 
                if not user_num_em:
                        user_data = user.dict(exclude_unset=True)
                        for key, value in user_data.items():
                            setattr(verify, key, value)
                            # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
                        db.add(verify)
                        db.commit()

                        return {'message': 'Employee updated successfully.'} 
                else:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Employee. Mobile Number already exists')
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Employee. Mobile Number already exists')
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Employee. Mobile Number already exists')
                    
@router.post('/uploadProfile/{id}', status_code=status.HTTP_202_ACCEPTED)
async def upload_profile(id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    verify = db.query(Employee).filter(Employee.em_id == id).first()

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

    verify.em_pic = token_name
    db.add(verify)
    db.commit()

    file_url = "localhost:8000" + generate_name[1:]
    return {"status": "ok", "filename": file_url}

@router.get('/deactivate/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Employee to cancel is not found')
    else:
        db.query(User_credential).filter(User_credential.user_id == id).update({'user_status': "Inactive"})
        
    db.commit()
    
    time.sleep(1)  
    response = RedirectResponse(url='/admin/employee/', status_code=302)
    return response

#ORDER ROUTES
@router.post('/{id}')
async def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(Orders).filter(Orders.order_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Order to cancel is not found')
    else:
        db.query(Orders).filter(Orders.order_id == id).update({'order_status': "For Pick-up"})

    db.commit()

    users = db.query(User_credential).filter(User_credential.user_id == cancel.order_userid).first()

    await for_pickup([users.user_email])

    return

#PAYMENT ROUTES
@router.post('/orderPayment/{id}')
def payment(id: str, pay: PaymentBase, db: Session = Depends(get_db)):
    payment = db.query(Orders).filter(Orders.order_id == id).first()

    if pay.order_payment == payment.order_total:
        db.query(Orders).filter(Orders.order_id == id).update({'order_status': "Paid"})
        db.commit()

        return {'message': 'Success'}
    else:
        raise HTTPException(404, 'Insufficient Payment')