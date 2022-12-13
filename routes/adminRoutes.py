from fastapi import APIRouter, Depends, Response, Request, Cookie, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_token, check_admin
from models.clientModel import Client
from models.timeSlotModel import Timeslot
from models.appointmentModel import Appointment
from schemas.appointmentSchema import AppointmentBase, AppointmentUpdate
from schemas.userCredentialSchema import LoginForm, UserBase, ClientBase, DoctorBase, EmployeeBase, UserRead, updateUser, TokenData
from schemas.clientSchema import clientUpdate
from schemas.serviceSchema import ServiceBas, ServiceBase
from models.userCredentialModel import User_credential
from models.clientModel import Client
from models.doctorModel import Doctor
from models.employeeModel import Employee
from models.productsModel import Product
from models.serviceModel import Service
import datetime as dt
from datetime import timedelta
from for_email import *
import random
import string
from jose import jwt
from typing import Optional, List
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
import time

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

    return result_str
def randoms():
    S = 7  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
    return ran

secret = 'a very shady secret'
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(check_admin)]
)

templates = Jinja2Templates(directory="templates")

@router.get("/")
def registration(request: Request):
    return templates.TemplateResponse("adminside/admin.html", {"request": request})

@router.get('/user_credentials', response_class=HTMLResponse)
def user_credentials(request: Request, db: Session = Depends(get_db)):
    try:
        credentials = db.query(User_credential).all()
        return templates.TemplateResponse('adminside/adminUsers.html', {
            'request': request,
            'credential': credentials
        })
    except Exception as e:
        print(e)

@router.get('/appointments')
def appointments(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Appointment).all()
        return templates.TemplateResponse('adminside/adminAppointments.html', {
            'request': request,
            'appointments': query
        })
    except Exception as e:
        print(e)

@router.get('/schedules')
def schedules(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Timeslot).all()
        return templates.TemplateResponse('adminside/adminSchedules.html', {
            'request': request,
            'schedules': query
        })

    except Exception as e:
        print(e)

@router.get('/reports')
def reports(request: Request):
    return templates.TemplateResponse("adminside/adminReports.html", {"request": request})

@router.get('/products', response_class=HTMLResponse)
def products(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Product).all()
        return templates.TemplateResponse('adminside/adminProducts.html', {
            'request': request,
            'product': query
        })

    except Exception as e:
        print(e)

@router.get('/services', response_class=HTMLResponse)
def services(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Service).all()
        return templates.TemplateResponse('adminside/adminServices.html', {
            'request': request,
            'service': query
        })

    except Exception as e:
        print(e)

@router.post('/services', response_class=HTMLResponse)
def store(response: Response, form_data: ServiceBase, db: Session = Depends(get_db)):

    if db.query(Service).filter(Service.service_name == form_data.service_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create service. Service already exists')
    else: 
        to_store = Service(
            service_name = form_data.service_name,
            service_price = form_data.service_price,
            service_description = form_data.service_description,
            service_status = "Active"
        )

    db.add(to_store)
    db.commit()
    # time.sleep(1)

    # response = RedirectResponse(url='/admin/services', status_code=302)

    return

@router.get('/doctor', response_class=HTMLResponse)
def doctor(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(User_credential, Doctor).join(Doctor).all()
        return templates.TemplateResponse('adminside/adminDoctor.html', {
            'request': request,
            'doctor': query
        })

    except Exception as e:
        print(e)

@router.post('/doctor', response_class=HTMLResponse)
def createDoctor(response: Response, form_data: DoctorBase, db: Session = Depends(get_db)):
    user_duplicate = db.query(User_credential).filter(User_credential.user_username == form_data.user_username).first()
    user_email_dup = db.query(User_credential).filter(User_credential.user_email == form_data.user_email).first()

    user_num_cl = db.query(Client).filter(Client.cl_contactNo == form_data.dt_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == form_data.dt_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == form_data.dt_contactNo).first()

    if not user_num_cl: 
        if not user_num_doc: 
            if not user_num_em:
                if not user_duplicate:
                    if not user_email_dup:
                        to_store = User_credential(
                            user_username = form_data.user_username,
                            user_password = password_hash(form_data.user_password),
                            user_email = form_data.user_email,
                            user_type = "Doctor"   
                        )
                        db.add(to_store)
                        db.commit()
                        db.refresh(to_store)   
                        to_employee = Doctor(
                            dt_pic = "ASD",
                            dt_firstName = form_data.dt_firstName,
                            dt_middleName = form_data.dt_middleName,
                            dt_lastName = form_data.dt_lastName,
                            dt_fullName = form_data.dt_firstName + " " + form_data.dt_middleName + " " + form_data.dt_lastName,
                            dt_houseNo = form_data.dt_houseNo,
                            dt_street = form_data.dt_street,
                            dt_brgy = form_data.dt_brgy,
                            dt_city = form_data.dt_city,
                            dt_address = form_data.dt_houseNo + " " + form_data.dt_street + " " + form_data.dt_brgy + " " + form_data.dt_city,
                            dt_status = "Active",
                            dt_contactNo = form_data.dt_contactNo,
                            dt_user_credential = to_store.user_id,
                            # cl_created_by = client.cl_created_by,
                            # cl_updated_by = client.cl_updated_by
                        )
                        db.add(to_employee)
                        db.commit()
                        db.refresh(to_employee)

                        # time.sleep(1)

                        # response = RedirectResponse(url='/admin/doctor', status_code=302)

                        return
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


@router.get('/employee', response_class=HTMLResponse)
def employee(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(User_credential, Employee).join(Employee).all()
        return templates.TemplateResponse('adminside/adminEmployee.html', {
            'request': request,
            'employee': query
        })

    except Exception as e:
        print(e)

@router.post('/employee', response_class=HTMLResponse)
def createEmployee(response: Response, form_data: EmployeeBase, db: Session = Depends(get_db)):
    user_duplicate = db.query(User_credential).filter(User_credential.user_username == form_data.user_username).first()
    user_email_dup = db.query(User_credential).filter(User_credential.user_email == form_data.user_email).first()

    user_num_cl = db.query(Client).filter(Client.cl_contactNo == form_data.em_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == form_data.em_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == form_data.em_contactNo).first()

    if not user_num_cl: 
        if not user_num_doc: 
            if not user_num_em:
                if not user_duplicate:
                    if not user_email_dup:
                        to_store = User_credential(
                            user_username = form_data.user_username,
                            user_password = password_hash(form_data.user_password),
                            user_email = form_data.user_email,
                            user_type = "Employee"   
                        )
                        db.add(to_store)
                        db.commit()
                        db.refresh(to_store)   
                        to_employee = Employee(
                            em_pic = "ASD",
                            em_firstName = form_data.em_firstName,
                            em_middleName = form_data.em_middleName,
                            em_lastName = form_data.em_lastName,
                            em_fullName = form_data.em_firstName + " " + form_data.em_middleName + " " + form_data.em_lastName,
                            em_houseNo = form_data.em_houseNo,
                            em_street = form_data.em_street,
                            em_brgy = form_data.em_brgy,
                            em_city = form_data.em_city,
                            em_address = form_data.em_houseNo + " " + form_data.em_street + " " + form_data.em_brgy + " " + form_data.em_city,
                            em_status = "Active",
                            em_contactNo = form_data.em_contactNo,
                            em_user_credential = to_store.user_id,
                            # cl_created_by = client.cl_created_by,
                            # cl_updated_by = client.cl_updated_by
                        )
                        db.add(to_employee)
                        db.commit()
                        db.refresh(to_employee)

                        # time.sleep(1)

                        # response = RedirectResponse(url='/admin/employee', status_code=302)

                        return
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

@router.get('/client', response_class=HTMLResponse)
def createClient(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(User_credential, Client).join(Client).all()
        return templates.TemplateResponse('adminside/adminClient.html', {
            'request': request,
            'client': query
        })

    except Exception as e:
        print(e)

@router.post('/client', response_class=HTMLResponse)
async def createClient(response: Response, form_data: ClientBase, db: Session = Depends(get_db)):
    print(form_data)
    user_duplicate = db.query(User_credential).filter(User_credential.user_username == form_data.user_username).first()
    user_email_dup = db.query(User_credential).filter(User_credential.user_email == form_data.user_email).first()
    user_num_cl = db.query(Client).filter(Client.cl_contactNo == form_data.cl_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == form_data.cl_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == form_data.cl_contactNo).first()

    if not user_num_cl: 
        if not user_num_doc: 
            if not user_num_em:
                if not user_duplicate:
                    if not user_email_dup:
                        to_store = User_credential(
                            user_username = form_data.user_username,
                            user_password = password_hash(form_data.user_password),
                            user_email = form_data.user_email,
                            user_type = "Client",
                            user_status = "Active"
                        )
                        db.add(to_store)
                        db.commit()
                        db.refresh(to_store)
                            
                        to_client = Client(
                            cl_pic = form_data.cl_pic,
                            cl_firstName = form_data.cl_firstName,
                            cl_middleName = form_data.cl_middleName,
                            cl_lastName = form_data.cl_lastName,
                            cl_fullName = form_data.cl_firstName + " " + form_data.cl_middleName + " " + form_data.cl_lastName,
                            cl_houseNo = form_data.cl_houseNo,
                            cl_street = form_data.cl_street,
                            cl_brgy = form_data.cl_brgy,
                            cl_city = form_data.cl_city,
                            cl_address = form_data.cl_houseNo + " " + form_data.cl_street + " " + form_data.cl_brgy + " " + form_data.cl_city,
                            cl_status = "Active",
                            cl_maritalStatus = form_data.cl_maritalStatus,
                            cl_birthdate = form_data.cl_birthdate,
                            cl_gender = form_data.cl_gender,
                            cl_contactNo = form_data.cl_contactNo,
                            cl_user_credential = to_store.user_id,
                            # cl_created_by = client.cl_created_by,
                            # cl_updated_by = client.cl_updated_by
                        )
                        db.add(to_client)
                        db.commit()

                        # await send_email([form_data.user_email], form_data.user_username)

                        # time.sleep(3)
                        # response = RedirectResponse(url='/admin/client', status_code=302)
                        return 
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

@router.post("/update/employee/{employees.em_id}",response_class=HTMLResponse)
async def updateEmployee(response: Response, form_data: EmployeeBase = Depends(EmployeeBase.as_form), db: Session = Depends(get_db)):
    
    id = db.query(EmployeeBase).filter(EmployeeBase.em_id == form_data.em_id).first()

    # update(id)
    time.sleep(1)
    response = RedirectResponse(url='/admin/client', status_code=302)
    return response

# @router.post('/update/client/{id}', response_class=clientUpdate)
# async def update(id: str, user: clientUpdate, db: Session = Depends(get_db)):
#     verify = db.query(Client).filter(Client.cl_id == id).first()
    
#     if not verify:
#         raise HTTPException(404, 'User to update is not found')

#     user_num_cl = db.query(Client).filter(Client.cl_contactNo == user.cl_contactNo).first()
#     user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == user.cl_contactNo).first()
#     user_num_em = db.query(Employee).filter(Employee.em_contactNo == user.cl_contactNo).first()
    
#     if not user_num_cl: 
#         if not user_num_doc: 
#             if not user_num_em:
#                     user_data = user.dict(exclude_unset=True)
#                     for key, value in user_data.items():
#                         setattr(verify, key, value)
#                         # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
#                     db.add(verify)
#                     db.commit()

#             else:
#                 raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')
#         else:
#             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')
#     else:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')
        
#     return {'message': 'Client updated successfully.'} 

@router.get('/appointment')
def appointments(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Appointment).all()
        query1 = db.query(Service).all()
        query2 = db.query(Timeslot).all()
        applen = int(len(query))
        serlen = int(len(query1))
        serlist = [(serlen)]
        applist = [(applen)]
        timlen = int(len(query2))
        timlist = [(timlen)]
        print(applist)
        
        print(applen)
        lst_all = query + query1 + query2 + applist + serlist + timlist
        print(lst_all)
        return templates.TemplateResponse('adminside/adminAppointments.html', {
            'request': request,
            'appointments': lst_all
        })
        
    except Exception as e:
        print(e)

@router.post('/appointment', response_class=HTMLResponse)
async def store(form_data: AppointmentBase = Depends(AppointmentBase.as_form), token: str = Cookie('token'), db: Session = Depends(get_db)):
    token = jwt.decode(token, secret, algorithms=['HS256'])

    serbisyo = db.query(Service).filter(Service.service_id == form_data.ap_serviceType).first()

    oras = db.query(Timeslot).filter(Timeslot.slot_id == form_data.ap_slotID).first()

    cliente = db.query(Client).filter(Client.cl_user_credential == token["id"]).first()

    simula = oras.slot_time

    umpisa = dt.datetime.strptime(f'{simula}', '%H:%M:%S')
    
    hangganan = umpisa + timedelta(hours=1)

    sched = db.query(Appointment).filter(Appointment.ap_slotID == form_data.ap_slotID).all()

    bilang = int(len(sched))

    kumpara = int(oras.slot_capacity)

    if bilang > kumpara-1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot schedule Appointment. Reached maximum capacity')

    to_store = Appointment(
        ap_number = randoms(),
        ap_clientID = token["id"],
        ap_startTime = umpisa,
        ap_clientName = cliente.cl_fullName,
        ap_date = oras.slot_date,
        ap_endTime = hangganan,
        ap_status = "Unpaid",
        ap_type = form_data.ap_type,
        ap_service = serbisyo.service_name,
        ap_comorbidity = form_data.ap_comorbidity,
        ap_serviceType = serbisyo.service_id,
        ap_amount = serbisyo.service_price,
        ap_slotID = oras.slot_id
    )

    db.add(to_store)
    db.commit()
    await send_appointment([token["email"]], to_store.ap_clientName, to_store.ap_date, to_store.ap_startTime, to_store.ap_endTime, to_store.ap_service, to_store.ap_amount)
    time.sleep(1)

    response = RedirectResponse(url='appointment', status_code=302)

    return response

@router.get('/profile')
def profile(request: Request):
    return templates.TemplateResponse("adminside/pro-profile.html", {"request": request})

@router.get('/logout')
def logout(response: Response):
    response = RedirectResponse(url='/auth', status_code=307)
    response.delete_cookie('token')
    return response
# @router.get('/logout', response_class=HTMLResponse)
# def protected_route(request: Request, user=Depends(manager)):
#     resp = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
#     manager.set_cookie(resp, "")
#     return resp