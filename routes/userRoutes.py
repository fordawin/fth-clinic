from fastapi import APIRouter, Depends, HTTPException, Cookie, Request, Response, status
from dotenv import dotenv_values
from models.prescriptionModel import Prescription
from schemas.userCredentialSchema import LoginForm, TokenData, ClientBase
from models.userCredentialModel import User_credential
from schemas.appointmentSchema import AppointmentBase, Sched
from models.appointmentModel import Appointment
from models.timeSlotModel import Timeslot
from models.serviceModel import Service
from models.clientModel import Client
from models.doctorModel import Doctor
from models.employeeModel import Employee
from models.productsModel import Product
from models.ordersModel import Orders
from sqlalchemy.orm import Session
from schemas.userSchema import CreateUser
from database import get_db
from dependencies import get_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from passlib.context import CryptContext
from jose import jwt
import datetime as dt
from datetime import timedelta
import random
import string
import time
from for_email import *

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

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

config_credentials = dict(dotenv_values(".env"))

secret = config_credentials["SECRET"]

def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)


router = APIRouter(
    prefix='/users',
    tags=['users']
)

templates = Jinja2Templates(directory="templates")

@router.get("/")
def registration(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Timeslot).all()
        query1 = db.query(Service).all()
        return templates.TemplateResponse('clientside/home.html', {
            'request': request,
            'dates': query,
            'service': query1
        })
    except Exception as e:
        print(e)

@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("clientside/login.html", {"request": request})

@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse("clientside/about.html", {"request": request})

@router.get("/about2")
def about(request: Request):
    return templates.TemplateResponse("clientside/about_after_login.html", {"request": request})


@router.post('/login', response_class=HTMLResponse)
async def login(response: Response, form_data: LoginForm, db: Session = Depends(get_db)):
    user = db.query(User_credential).filter(User_credential.user_email == form_data.user_email).first()
    if user:
        match = password_verify(form_data.user_password, user.user_password)
        if match:
            data = TokenData(id = user.user_id, email = user.user_email, type = user.user_type)
            token = jwt.encode(dict(data), secret)
            # response = RedirectResponse(url='appointments', status_code=302)
            response.set_cookie('token', token, httponly=True)
            response.set_cookie('type', user.user_type, httponly=False)
            return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect Username or Password"
    )

@router.post("/home2")
def read_form_post(request: Request, form_data: Sched, db: Session = Depends(get_db)):
    query1 = db.query(Service).all()
    verify = db.query(Timeslot).filter(Timeslot.slot_date == form_data.slot_date).first()
    # Here, you can add your logic to generate the schedule based on the selected date
    if not verify:
        return {"There's no schedule for today "}
    schedule = db.query(Timeslot).filter(Timeslot.slot_date == form_data.slot_date).all()
    # We'll just return a dummy schedule for now
    # schedule = ["10:00 AM - 11:00 AM", "1:00 PM - 2:00 PM", "4:00 PM - 5:00 PM"]
    print(schedule)

    return templates.TemplateResponse("clientside/home_after_login.html", {
        "request": request,
        'services': query1,
        'timeslots': schedule
    })
    
 

@router.get("/home2")
def home(request: Request, db: Session = Depends(get_db)):
    query1 = db.query(Service).all()
    query2 = db.query(Timeslot).all()
    return templates.TemplateResponse('clientside/home_after_login.html', {
        'request': request,
        'services': query1,
        'timeslots': query2
    })  

@router.post('/home3', response_class=HTMLResponse)
async def home(form_data: AppointmentBase, token: str = Cookie('token'), db: Session = Depends(get_db)):
    token = jwt.decode(token, secret, algorithms=['HS256'])

    serbisyo = db.query(Service).filter(Service.service_id == form_data.ap_serviceType).first()

    oras = db.query(Timeslot).filter(Timeslot.slot_id == form_data.ap_slotID).first()

    cliente = db.query(Client).filter(Client.cl_user_credential == token["id"]).first()

    simula = oras.slot_start
    
    hangganan = oras.slot_end

    sched = db.query(Appointment).filter(Appointment.ap_slotID == form_data.ap_slotID).all()

    bilang = int(len(sched))

    kumpara = int(oras.slot_capacity)

    if bilang > kumpara-1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot schedule Appointment. Reached maximum capacity')

    to_store = Appointment(
        ap_number = randoms(),
        ap_clientID = token["id"],
        ap_startTime = simula,
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

    response = RedirectResponse(url='/users/appointments', status_code=302)

    return response

@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("clientside/register.html", {"request": request})

@router.post('/register', response_class=HTMLResponse)
async def register(response: Response, form_data: ClientBase, db: Session = Depends(get_db)):
    
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
                            # cl_created_by = client.cl_created_by,
                            # cl_updated_by = client.cl_updated_by
                        )
                        db.add(to_client)
                        db.commit()

                        await send_email([form_data.user_email], form_data.cl_firstName, form_data.cl_middleName, form_data.cl_lastName)

                        time.sleep(5)
                        response = RedirectResponse(url='login', status_code=302)
                        return response
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

@router.get("/appointments")
def appointment(request: Request, token: str = Cookie('token'), db: Session = Depends(get_db)):
    token = jwt.decode(token, secret, algorithms=['HS256'])
    query = db.query(Appointment).all()
    query1 = db.query(Prescription).all()
    id = [token["id"]]
    lst_all = query + query1 + id
    print(lst_all)
    try:
        return templates.TemplateResponse('clientside/appointment.html', {
            'request': request,
            'appointment': lst_all
        })
    except Exception as e:
        print(e)

@router.get("/profile")
def profile(request: Request, token: str = Cookie('token'), db: Session = Depends(get_db)):
    query = db.query(Client).all()
    query1 = db.query(Appointment).all()
    query2 = db.query(User_credential).all()
    query3 = db.query(Orders).all()
    token = jwt.decode(token, secret, algorithms=['HS256'])
    id = [token["id"]]
    lst_all = query + query1 + query2 + query3 + id
    print(lst_all)
    try:
        return templates.TemplateResponse('clientside/profile.html', {
                'request': request,
                'profile': lst_all
            })
    except Exception as e:
        print(e)

@router.get("/contact")
def contact(request: Request):
    try:
        return templates.TemplateResponse('clientside/contact.html', {
            'request': request
        })
    except Exception as e:
        print(e)

@router.get("/contact2")
def contact(request: Request):
    try:
        return templates.TemplateResponse('clientside/contact_after_login.html', {
            'request': request
        })
    except Exception as e:
        print(e)

@router.get("/product")
def shop(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Product).all()
        return templates.TemplateResponse('clientside/product.html', {
            'request': request,
            'product_list': query
        })
    except Exception as e:
        print(e)

@router.get("/product2")
def shop(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Product).all()
        return templates.TemplateResponse('clientside/product_after_login.html', {
            'request': request,
            'product_list': query
        })
    except Exception as e:
        print(e)

@router.get("/orders")
def order(request: Request, token: str = Cookie('token'), db: Session = Depends(get_db)):
    token = jwt.decode(token, secret, algorithms=['HS256'])
    query = db.query(Orders).all()
    id = [token["id"]]
    lst_all = query + id
    print(lst_all)
    try:
        return templates.TemplateResponse('clientside/orders.html', {
            'request': request,
            'order_list': lst_all
        })
    except Exception as e:
        print(e)

@router.get("/forgot")
def home(request: Request):
    return templates.TemplateResponse('clientside/forgot.html', {
        'request': request,
    })  

@router.get('/logout')
def logout(response: Response):
    response = RedirectResponse(url='/users/login', status_code=307)
    response.delete_cookie('token')
    return response