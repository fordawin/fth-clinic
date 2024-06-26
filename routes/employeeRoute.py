from fastapi import APIRouter, Depends, HTTPException, Cookie, status, Response, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
from schemas.employeeSchema import employeeUpdate
from schemas.orderSchema import PaymentBase as OrderPayment
from schemas.paymentSchema import PaymentBase, PaymentUpdate
from schemas.userCredentialSchema import UserBase, EmployeeBase
from schemas.orderSchema import PaymentBase as PaymentB
from models.userCredentialModel import User_credential
from models.timeSlotModel import Timeslot
from models.appointmentModel import Appointment
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
from systemlogs import *
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
async def update(id: str, user: employeeUpdate, db: Session = Depends(get_db)):
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
        await system_logs("Dr.", verify.em_fullName, f"Updated their profile.")     
        db.add(verify)
        db.commit()
    else:
        if not user_num_cl: 
            if not user_num_doc: 
                if not user_num_em:
                        user_data = user.dict(exclude_unset=True)
                        for key, value in user_data.items():
                            setattr(verify, key, value)
                            
                        db.add(verify)
                        db.commit()
                        await system_logs("Dr.", verify.em_fullName, f"Updated their profile.") 
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
async def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Employee to cancel is not found')
    else:
        db.query(User_credential).filter(User_credential.user_id == id).update({'user_status': "Inactive"})

    await system_logs("Emoloyee", cancel.user_username, f"Deactivated their account.")     
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

    users = db.query(User_credential).filter(User_credential.user_id == cancel.order_userid).first()
    await system_logs("Employee", users.user_username, f"Approved an order.") 
    await for_pickup([users.user_email])
    db.commit()

    return

#PAYMENT ROUTES
@router.post('/orderPayment/{id}')
async def payment(id: str, pay: PaymentB, db: Session = Depends(get_db)):
    print(pay)
    payment = db.query(Orders).filter(Orders.order_id == id).first()

    if pay.order_payment == payment.order_total:
        db.query(Orders).filter(Orders.order_id == id).update({'order_status': "Paid"})
        db.commit()
        users = db.query(User_credential).filter(User_credential.user_id == payment.order_userid).first()
        await system_logs("Employee", users.user_username, f"Paid an order.")
        return {'message': 'Success'}
    else:
        raise HTTPException(402, 'Insufficient Payment')


#APPOINTMENT ROUTES
@router.get('/approveCancel/{id}')
async def approve(id: str, db: Session = Depends(get_db)):
    cancel = db.query(Appointment).filter(Appointment.ap_id == id).first()
    slot = db.query(Timeslot).filter(Timeslot.slot_id == cancel.ap_slotID).first()

    if not cancel:
        raise HTTPException(404, 'Appointment to cancel is not found')
    else:
        slotAdd = int(slot.slot_capacity) + 1
        db.query(Timeslot).filter(Timeslot.slot_id == cancel.ap_slotID).update({'slot_capacity': slotAdd})
        db.query(Appointment).filter(Appointment.ap_id == id).update({'ap_status': "Cancelled"})

    users = db.query(User_credential).filter(User_credential.user_id == cancel.ap_clientID).first()   
    await system_logs("Employee", users.user_username, f"Approved a request for cancellation of appointment.")
    await appointment_cancel([users.user_email])
    db.commit()

    return

@router.get('/denyCancel/{id}')
async def deny(id: str, db: Session = Depends(get_db)):
    cancel = db.query(Appointment).filter(Appointment.ap_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Appointment to cancel is not found')
    else:
        db.query(Appointment).filter(Appointment.ap_id == id).update({'ap_status': "Unpaid"})
        users = db.query(User_credential).filter(User_credential.user_id == cancel.ap_clientID).first()   
        await system_logs("Employee", users.user_username, f"Denied a request for cancellation of appointment.")

    db.commit()

    return