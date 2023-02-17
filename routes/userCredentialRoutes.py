from fastapi import APIRouter, Depends, HTTPException, Cookie, status, Response, Request
from dotenv import dotenv_values
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from models.appointmentModel import Appointment
from schemas.userCredentialSchema import UserBase, ClientBase, DoctorBase, EmployeeBase, UserRead, updateUser, TokenData, forgotPass
from models.userCredentialModel import User_credential
from models.adminModel import Admin
from models.clientModel import Client
from models.doctorModel import Doctor
from models.employeeModel import Employee
from database import get_db
from typing import List
from dependencies import get_token
from passlib.context import CryptContext
from sqlalchemy import or_
from datatables import DataTable
from for_email import *
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt
import time
import random
import string


templates = Jinja2Templates(directory="templates")

config_credentials = dict(dotenv_values(".env"))

secret = config_credentials["SECRET"]
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)

def randoms():
    S = 7  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
    return ran

router = APIRouter(
    prefix='/usercredential',
    tags=['user credential']
)

@router.get('/{id}', status_code=status.HTTP_202_ACCEPTED)
def findOne(id: str, db: Session = Depends(get_db)):

    user = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'User does not exists')

    if user.user_type == "Client":
        credential = db.query(Client).filter(Client.cl_user_credential == id).first()
    elif user.user_type == "Employee":
        credential = db.query(Employee).filter(Employee.em_user_credential == id).first()
    else:
        credential = db.query(Doctor).filter(Doctor.dt_user_credential == id).first()
        
    return {'user': user, 'credential': credential}

@router.post('/admin')
def createAdmin(user: UserBase, db: Session = Depends(get_db)):
    to_store = User_credential(
        user_username = user.user_username,
        user_password = password_hash(user.user_password),
        user_email = user.user_email,
        user_type = "Admin",
        user_status = "Active" 
    )
    db.add(to_store)
    db.commit()
    db.refresh(to_store)
    to_admin = Admin(
        ad_user_credential = to_store.user_id
    )

    db.add(to_admin)
    db.commit()

@router.post('/client')
async def createClient(user: UserBase, client: ClientBase, db: Session = Depends(get_db)):
    
    user_duplicate = db.query(User_credential).filter(User_credential.user_username == user.user_username).first()
    user_email_dup = db.query(User_credential).filter(User_credential.user_email == user.user_email).first()
    user_num_cl = db.query(Client).filter(Client.cl_contactNo == client.cl_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == client.cl_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == client.cl_contactNo).first()

    if not user_num_cl: 
        if not user_num_doc: 
            if not user_num_em:
                if not user_duplicate:
                    if not user_email_dup:
                        to_store = User_credential(
                            user_username = user.user_username,
                            user_password = password_hash(user.user_password),
                            user_email = user.user_email,
                            user_type = "Client",
                            user_status = "Inactive" 
                        )
                        db.add(to_store)
                        db.commit()
                        db.refresh(to_store)
                            
                        to_client = Client(
                            cl_pic = client.cl_pic,
                            cl_firstName = client.cl_firstName,
                            cl_middleName = client.cl_middleName,
                            cl_lastName = client.cl_lastName,
                            cl_fullName = client.cl_firstName + " " + client.cl_middleName + " " + client.cl_lastName,
                            cl_houseNo = client.cl_houseNo,
                            cl_street = client.cl_street,
                            cl_brgy = client.cl_brgy,
                            cl_city = client.cl_city,
                            cl_address = client.cl_houseNo + " " + client.cl_street + " " + client.cl_brgy + " " + client.cl_city,
                            cl_status = "Active",
                            cl_maritalStatus = client.cl_maritalStatus,
                            cl_birthdate = client.cl_birthdate,
                            cl_gender = client.cl_gender,
                            cl_contactNo = client.cl_contactNo,
                            cl_user_credential = to_store.user_id,
                            # cl_created_by = client.cl_created_by,
                            # cl_updated_by = client.cl_updated_by
                        )
                        db.add(to_client)
                        db.commit()

                        await send_email([user.user_email], user.user_username)
                        return {'message' : "Successfully Registered"}
                    else:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Email already exists')       
                else:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Username already exists')
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Mobile Number already exists')
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Mobile Number already exists')
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Mobile Number already exists')

@router.post('/doctor')
def createDoctor(user: UserBase, doctor: DoctorBase, db: Session = Depends(get_db)):
    user_duplicate = db.query(User_credential).filter(User_credential.user_username == user.user_username).first()
    user_email_dup = db.query(User_credential).filter(User_credential.user_email == user.user_email).first()

    user_num_cl = db.query(Client).filter(Client.cl_contactNo == doctor.dt_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == doctor.dt_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == doctor.dt_contactNo).first()

    if not user_num_cl: 
        if not user_num_doc: 
            if not user_num_em:
                if not user_duplicate:
                    if not user_email_dup:
                        to_store = User_credential(
                            user_username = user.user_username,
                            user_password = password_hash(user.user_password),
                            user_email = user.user_email,
                            user_type = "Doctor"  
                        )
                        db.add(to_store)
                        db.commit()
                        db.refresh(to_store)
                            
                        to_doctor = Doctor(
                            dt_firstName = doctor.dt_firstName,
                            dt_pic = "ASD",
                            dt_middleName = doctor.dt_middleName,
                            dt_lastName = doctor.dt_lastName,
                            dt_fullName = doctor.dt_firstName + " " + doctor.dt_middleName + " " + doctor.dt_lastName,
                            dt_houseNo = doctor.dt_houseNo,
                            dt_street = doctor.dt_street,
                            dt_brgy = doctor.dt_brgy,
                            dt_city = doctor.dt_city,
                            dt_address = doctor.dt_houseNo + " " + doctor.dt_street + " " + doctor.dt_brgy + " " + doctor.dt_city,
                            dt_status = "Active",
                            dt_fee = doctor.dt_fee,
                            dt_specialization = doctor.dt_specialization,
                            dt_contactNo = doctor.dt_contactNo,
                            dt_user_credential = to_store.user_id,
                            # cl_created_by = client.cl_created_by,
                            # cl_updated_by = client.cl_updated_by
                        )
                        db.add(to_doctor)
                        db.commit()
                        return {"Doctor Successfully Registered"}
                    else:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Email already exists')       
                else:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Username already exists')
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Mobile Number already exists')
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Mobile Number already exists')
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Mobile Number already exists')

@router.post('/employee')
def createEmployee(user: UserBase, employee: EmployeeBase, db: Session = Depends(get_db)):
    user_duplicate = db.query(User_credential).filter(User_credential.user_username == user.user_username).first()
    user_email_dup = db.query(User_credential).filter(User_credential.user_email == user.user_email).first()

    user_num_cl = db.query(Client).filter(Client.cl_contactNo == employee.em_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == employee.em_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == employee.em_contactNo).first()

    if not user_num_cl: 
        if not user_num_doc: 
            if not user_num_em:
                if not user_duplicate:
                    if not user_email_dup:
                        to_store = User_credential(
                            user_username = user.user_username,
                            user_password = password_hash(user.user_password),
                            user_email = user.user_email,
                            user_type = "Employee"   
                        )
                        db.add(to_store)
                        db.commit()
                        db.refresh(to_store)   
                        to_employee = Employee(
                            em_pic = "ASD",
                            em_firstName = employee.em_firstName,
                            em_middleName = employee.em_middleName,
                            em_lastName = employee.em_lastName,
                            em_fullName = employee.em_firstName + " " + employee.em_middleName + " " + employee.em_lastName,
                            em_houseNo = employee.em_houseNo,
                            em_street = employee.em_street,
                            em_brgy = employee.em_brgy,
                            em_city = employee.em_city,
                            em_address = employee.em_houseNo + " " + employee.em_street + " " + employee.em_brgy + " " + employee.em_city,
                            em_status = "Active",
                            em_contactNo = employee.em_contactNo,
                            em_user_credential = to_store.user_id,
                            # cl_created_by = client.cl_created_by,
                            # cl_updated_by = client.cl_updated_by
                        )
                        db.add(to_employee)
                        db.commit()
                        db.refresh(to_employee)

                        return {"Employee Successfully Registered"}
                    else:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Email already exists')       
                else:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Username already exists')
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Mobile Number already exists')
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Mobile Number already exists')
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create user. Mobile Number already exists')

@router.post('/{id}', response_model=updateUser)
def update(id: str, user: updateUser = Depends(updateUser.as_form), db: Session = Depends(get_db)):
    verify = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not verify:
        raise HTTPException(404, 'User to update is not found')
    
    user_email_dup = db.query(User_credential).filter(User_credential.user_email == user.user_email).first()
    if user_email_dup:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update user. Email already exists')

    user_name_dup = db.query(User_credential).filter(User_credential.user_username == user.user_username).first()
    if user_name_dup:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update user. Email already exists')  

    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(verify, key, value)
    # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
    db.add(verify)
    db.commit()

    time.sleep(3)
    response = RedirectResponse(url='/users/profile', status_code=302)
    return response

@router.post('/pass/{id}')
def update_password(id: str, user: updateUser, db: Session = Depends(get_db)):
    verify = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not verify:
        raise HTTPException(404, 'User to update is not found')
    
    old_password = password_verify(user.old_password, verify.user_password)

    if not old_password:
        raise HTTPException(404, 'Old Password did not match')
    
    if user.user_password == user.user_passwordre:
        pw = password_hash(user.user_password)
        user.user_password = pw
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
        # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
        db.add(verify)
        db.commit()

        # time.sleep(1)  
        # response = RedirectResponse(url='/users/profile', status_code=302)
        return
    else:
        raise HTTPException(404, 'Passwords did not match')

@router.post('/login')
def Login(form: UserBase, response: Response, db: Session = Depends(get_db)):
    try:
        user = db.query(User_credential).filter(User_credential.user_email == form.user_email).first()
        if user:
            match = password_verify(form.user_password, user.user_password)
            if match:
                data = TokenData(email = user.user_email, type = user.user_type, id = user.user_id)
                token = jwt.encode(dict(data), secret)
                response.set_cookie('token', token, httponly=True)
                return {'message': 'Log In Success!', 'token': token}
        
        return {'message': 'User not found.'}
    except Exception as e:
        print(e)

@router.post('/logout')
def logout(response: Response):
    response.delete_cookie('token')
    return {'message': 'Logout Success!'}

@router.post('/deactivate/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Appointment to cancel is not found')
    else:
        db.query(Appointment).filter(Appointment.ap_id == id).update({'ap_status': "Canceled"})
        
    db.commit()

@router.get('/deactivate/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not cancel:
        raise HTTPException(404, 'User to cancel is not found')
    else:
        db.query(User_credential).filter(User_credential.user_id == id).update({'user_status': "Inactive"})
        
    db.commit()
    time.sleep(1)  
    response = RedirectResponse(url='/admin/user_credentials/', status_code=302)
    return response

@router.post('/forgotpassword/')
async def forgotpass(form_data: forgotPass, db: Session = Depends(get_db)):
    emailChecking = db.query(User_credential).filter(User_credential.user_email == form_data.user_email).first()

    if not emailChecking:
        raise HTTPException(404, 'The email you have provided is not registered!')
    else:
        newPassword = randoms()
        db.query(User_credential).filter(User_credential.user_id == emailChecking.user_id).update({'user_password': password_hash(newPassword)})
        db.commit()
        await passwordChange([form_data.user_email], newPassword)
        return {'message': 'Password Changed!'}
        

