from fastapi import APIRouter, Depends, Response, Request, Cookie, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_token, check_admin
from models.clientModel import Client
from models.timeSlotModel import Timeslot
from models.appointmentModel import Appointment
from models.paymentModel import Payment
from schemas.paymentSchema import PaymentUpdate, PaymentBase as PaymentB
from schemas.employeeSchema import employeeUpdate
from schemas.timeSlotSchema import SlotBase, TimeSlotUpdate
from schemas.productSchema import productUpdate, ProductBase, Discount
from schemas.appointmentSchema import AppointmentBase, AppointmentUpdate
from schemas.userCredentialSchema import LoginForm, UserBase, ClientBase, DoctorBase, EmployeeBase, UserRead, updateUser, TokenData
from schemas.clientSchema import clientUpdate
from schemas.serviceSchema import ServiceBas, ServiceBase, updateService
from schemas.orderSchema import OrderBase, PaymentBase as PaymentOrder
from models.userCredentialModel import User_credential
from models.clientModel import Client
from models.doctorModel import Doctor
from models.ordersModel import Orders
from models.employeeModel import Employee
from models.productsModel import Product
from models.serviceModel import Service
from dotenv import dotenv_values
import datetime as dt
from datetime import timedelta, date
from for_email import *
import random
import string
from jose import jwt
from typing import Optional, List
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
import time

from fastapi.staticfiles import StaticFiles
from PIL import Image
import secrets

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

config_credentials = dict(dotenv_values(".env"))

secret = config_credentials["SECRET"]
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
def dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        pending = db.query(Appointment).filter(Appointment.ap_status == "Unpaid").all()
        paid = db.query(Appointment).filter(Appointment.ap_status == "Paid").all()
        cancel = db.query(Appointment).filter(Appointment.ap_status == "Canceled").all()
        appointment = db.query(Appointment).all()
        order = db.query(Orders).all()
        active_users = db.query(User_credential).filter(User_credential.user_status == "Active").all()

        order_pending = db.query(Orders).filter(Orders.order_status == "Pending").all()
        order_paid = db.query(Orders).filter(Orders.order_status == "Paid").all()
        order_cancel = db.query(Orders).filter(Orders.order_status == "Canceled").all()
        order_pickup = db.query(Orders).filter(Orders.order_status == "For Pick-up").all()

        return templates.TemplateResponse("adminside/admin.html", {
            "request": request,
            "pending": pending,
            "paid": paid,
            "active_users": active_users,
            "cancel": cancel,
            "appointments": appointment,
            "order_pending": order_pending,
            "order_paid": order_paid,
            "order_cancel": order_cancel,
            "order_pickup": order_pickup,
            "orders": order
        })

    except Exception as e:
        print(e)

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

@router.get('/deactivate/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(Appointment).filter(Appointment.ap_id == id).first()
    slot = db.query(Timeslot).filter(Timeslot.slot_id == cancel.ap_slotID).first()

    slotAdd = int(slot.slot_capacity) + 1

    if not cancel:
        raise HTTPException(404, 'Appointment to cancel is not found')
    else:
        db.query(Timeslot).filter(Timeslot.slot_id == cancel.ap_slotID).update({'slot_capacity': slotAdd})
        db.query(Appointment).filter(Appointment.ap_id == id).update({'ap_status': "Canceled"})
        
    db.commit()

    time.sleep(1)

    response = RedirectResponse(url='/admin/appointment', status_code=302)

    return response

@router.get('/reports')
def reports(request: Request):
    return templates.TemplateResponse("adminside/adminReports.html", {"request": request})

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

#EMPLOYEE ROUTE
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
                        )
                        db.add(to_employee)
                        db.commit()
                        db.refresh(to_employee)

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

@router.post('/employeeUpdate/{id}')
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

                        return {'message': 'Employee updated successfully.'} 
                else:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Employee. Mobile Number already exists')
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Employee. Mobile Number already exists')
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Employee. Mobile Number already exists')

@router.get('/employeeDeactivate/{id}')
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

#CLIENT ROUTE
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
                            user_points = 0,
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
                        )
                        db.add(to_client)
                        db.commit()
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

@router.get('/paymentPending')
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
        return templates.TemplateResponse('adminside/adminPayment.html', {
            'request': request,
            'appointments': lst_all
        })
        
    except Exception as e:
        print(e)

@router.get('/paymentDone')
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
        return templates.TemplateResponse('adminside/adminPaymentDone.html', {
            'request': request,
            'appointments': lst_all
        })
        
    except Exception as e:
        print(e)


@router.get('/profile')
def profile(request: Request):
    return templates.TemplateResponse("adminside/pro-profile.html", {"request": request})

@router.get('/logout')
def logout(response: Response):
    response = RedirectResponse(url='/users/login', status_code=307)
    response.delete_cookie('token')
    response.delete_cookie('type')
    return response

#SERVICE ROUTE
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
    return

@router.post('/updateService/{id}')
def update(id: str, user: updateService, db: Session = Depends(get_db)):
    verify = db.query(Service).filter(Service.service_id == id).first()

    if not verify:
        raise HTTPException(404, 'Service to update is not found')
    else:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
        db.add(verify)
        db.commit()

@router.get('/deactivateService/{id}')
def deactivateService(id: str, db: Session = Depends(get_db)):
    
    if not db.query(Service).filter(Service.service_id == id).update({'service_status': "Inactive"}):
        raise HTTPException(404, 'Service to delete is not found')

    db.commit()

    time.sleep(1)

    response = RedirectResponse(url='/admin/services', status_code=302)

    return response

#PRODUCTS ROUTE
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

@router.post('/defaultProduct')
async def store(request: Request, product: ProductBase = Depends(ProductBase.as_form), file: UploadFile = File(...), db: Session = Depends(get_db)):

    if db.query(Product).filter(Product.product_name == product.product_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create product. Product already exists')
    else: 
        FILEPATH = "static/images/"
        filename = file.filename
        extension = filename.split(".")[1]

        if extension not in ["png", "jpg", "PNG", "jpeg", "JPG", "JPEG"]:
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

        product_pic = token_name

        # file_url = "localhost:8000" + generate_name[1:]
        to_store = Product(
            product_name = product.product_name,
            product_pic = product_pic,
            product_price = product.product_price,
            product_quantity = product.product_quantity,
            product_discount = 0,
            product_type = "Default",
            product_description = product.product_description,
            product_status = "Active"
        )

        db.add(to_store)
        db.commit()

        response = RedirectResponse(url='/admin/products', status_code=302)

        return response

@router.post('/promoProduct')
async def store(request: Request, product: ProductBase = Depends(ProductBase.as_form), file: UploadFile = File(...), db: Session = Depends(get_db)):

    if db.query(Product).filter(Product.product_name == product.product_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create product. Product already exists')
    else: 
        FILEPATH = "static/images/"
        filename = file.filename
        extension = filename.split(".")[1]

        if extension not in ["png", "jpg", "PNG", "jpeg", "JPG", "JPEG"]:
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

        product_pic = token_name

        # file_url = "localhost:8000" + generate_name[1:]
        to_store = Product(
            product_name = product.product_name,
            product_pic = product_pic,
            product_price = product.product_price,
            product_quantity = product.product_quantity,
            product_discount = 0,
            product_type = "Promo",
            product_description = product.product_description,
            product_status = "Active"
        )

        db.add(to_store)
        db.commit()

        response = RedirectResponse(url='/admin/products', status_code=302)

        return response

@router.post('/productUpdate/{id}', response_model=productUpdate)
def update(id: str, user: productUpdate, db: Session = Depends(get_db)):
    verify = db.query(Product).filter(Product.product_id == id).first()

    if not verify:
        raise HTTPException(404, 'Product to update is not found')
    
    if db.query(Product).filter(Product.product_name == user.product_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Product. Product already exists')
    else:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
        db.add(verify)
        db.commit()

        return {'message': 'Product updated successfully.'} 

@router.get('/productDeactivate/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    # deletion = db.query(Product).filter(Product.product_id == id).first()

    if not db.query(Product).filter(Product.product_id == id).update({'product_status': "Inactive"}):
        raise HTTPException(404, 'Product to delete is not found')

    db.commit()
    
    time.sleep(1)

    response = RedirectResponse(url='/admin/products', status_code=302)

    return response

@router.post('/productDiscount/{id}')
def discount(id: str, product: Discount, db: Session = Depends(get_db)):
    db.expire_all()
    if not db.query(Product).filter(Product.product_id == id).update({'product_discount': product.product_discount}):
        raise HTTPException(404, 'Product not found')

    db.commit()
    return {'message': 'Discount successfully placed.'}

#SCHEDULE ROUTES
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

@router.post('/newSchedule')
def store(user: SlotBase, db: Session = Depends(get_db)):

    i = 0
    user.slot_number = user.slot_number + 1
    timestr = user.slot_daystart
    duration = str(user.slot_duration)
    durationHour = int(duration[1])
    durationM = str(duration[3]) + str(duration[4])
    durationMin = int(durationM)

    t1 = dt.datetime.strptime(timestr, '%H:%M')
    while i < user.slot_number-1:
        format = "%H:%M"
        time = t1 + timedelta(hours=i)
        if i == 0:
            timeStart = time + timedelta(hours=i*durationHour)
            timeEnd = timeStart + timedelta(hours=durationHour, minutes=durationMin)
            timeEnd = timeEnd.strftime(format)
            timeStart = timeStart.strftime(format)
            to_store = Timeslot(
                slot_capacity = user.slot_capacity,
                slot_start = timeStart,
                slot_end = timeEnd,
                slot_date = user.slot_date,
                slot_status = "Active"
            )
            db.add(to_store)
            db.commit()
        else:
            timeStarting = time + timedelta(hours=i*durationHour-i, minutes=i*durationMin)
            timeEnding = timeStarting + timedelta(hours=durationHour, minutes=durationMin)
            timeEnding = timeEnding.strftime(format)
            timeStarting = timeStarting.strftime(format)
            to_store = Timeslot(
                slot_capacity = user.slot_capacity,
                slot_start = timeStarting,
                slot_end = timeEnding,
                slot_date = user.slot_date,
                slot_status = "Active"
            )
            db.add(to_store)
            db.commit()
        i += 1
    return {'message': 'Success successfully.'}

@router.post('/updateSchedule/{id}')
def update(id: str, user: TimeSlotUpdate, db: Session = Depends(get_db)):
    verify = db.query(Timeslot).filter(Timeslot.slot_id == id).first()

    if not verify:
        raise HTTPException(404, 'Timeslot to update is not found')
    
    else:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
            db.add(verify)
            db.commit()
            
        return {'message': 'Updated successfully.'} 

@router.post('/deactivateSchedule/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(Timeslot).filter(Timeslot.slot_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Time Slot to cancel is not found')
    else:
        db.query(Timeslot).filter(Timeslot.slot_id == id).update({'slot_status': "Inactive"})
        db.commit()

#ORDER ROUTES
@router.get('/orderPending')
def employee(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Orders).all()
        return templates.TemplateResponse('adminside/adminOrderPending.html', {
            'request': request,
            'order_list': query
        })
        
    except Exception as e:
        print(e)

@router.get('/orderAcceptedNew')
def employee(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Orders).all()
        return templates.TemplateResponse('adminside/adminOrderAcceptedNew.html', {
            'request': request,
            'order_list': query
        })
        
    except Exception as e:
        print(e)

@router.get('/acceptOrder/{id}')
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

@router.get('/orderCancelled')
def employee(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Orders).all()
        return templates.TemplateResponse('adminside/adminOrderCancelled.html', {
            'request': request,
            'order_list': query
        })
        
    except Exception as e:
        print(e)

@router.get('/denyOrder/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(Orders).filter(Orders.order_id == id).first()
    product = db.query(Product).filter(Product.product_id == cancel.order_productid).first()
    
    quantity = int(cancel.order_quantity) + int(product.product_quantity)

    if not cancel:
        raise HTTPException(404, 'Order to cancel is not found')
    else:
        db.query(Product).filter(Product.product_id == cancel.order_productid).update({'product_quantity': quantity})
        db.query(Orders).filter(Orders.order_id == id).update({'order_status': "Cancelled"})

    db.commit()

    time.sleep(1)

    response = RedirectResponse(url='orderPending', status_code=302)

    return response

#PAYMENT ROUTES
@router.post('/orderPayment/{id}')
def payment(id: str, pay: PaymentOrder, db: Session = Depends(get_db)):
    payment = db.query(Orders).filter(Orders.order_id == id).first()

    if pay.order_payment == payment.order_total:
        db.query(Orders).filter(Orders.order_id == id).update({'order_status': "Paid"})
        db.commit()

        return {'message': 'Success'}
    else:
        raise HTTPException(404, 'Insufficient Payment')
    
@router.post('/appointmentPayment')
def store(form_data: PaymentB, db: Session = Depends(get_db)):

    query = db.query(Appointment).filter(Appointment.ap_id == form_data.payment_appointmentID).first()

    babayaran = int(query.ap_amount)

    bayad = int(form_data.payment_amount)

    points = db.query(User_credential).filter(User_credential.user_id == query.ap_clientID).first()

    addPoints = int(points.user_points) + 1

    if bayad < babayaran:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Insufficient Funds')
    else:
        db.query(Appointment).filter(Appointment.ap_id == form_data.payment_appointmentID).update({"ap_status": "Paid"})
        db.query(User_credential).filter(User_credential.user_id == points.user_id).update({"user_points": addPoints})
        
    to_store = Payment(
        payment_mode = form_data.payment_mode,
        payment_amount = form_data.payment_amount,
        payment_appointmentID = form_data.payment_appointmentID
    )
    db.add(to_store)
    db.commit()

    return {'message': 'Payment added successfully.'}