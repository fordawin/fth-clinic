from fastapi import FastAPI, APIRouter, Depends, HTTPException, Cookie, status, Response, Request
from sqlalchemy.orm import Session
from dotenv import dotenv_values
from schemas.userCredentialSchema import LoginForm, TokenData, forgotPass
from models.userCredentialModel import User_credential
from schemas.clientSchema import clientUpdate, clientUpdate2
from models.clientModel import Client
from models.employeeModel import Employee
from models.doctorModel import Doctor
from models.serviceModel import Service
from models.timeSlotModel import Timeslot
from models.appointmentModel import Appointment
from models.ordersModel import Orders
from models.productsModel import Product
from models.prescriptionModel import Prescription
from schemas.appointmentSchema import AppointmentBase
from database import get_db
from dependencies import get_token
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse, HTMLResponse
from for_email import *
import datetime
from datetime import timedelta
import time
import random
import string


#image upload
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image
import secrets

def randoms():
    S = 7  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
    return ran

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# app = FastAPI()
config_credentials = dict(dotenv_values(".env"))

secret = config_credentials["SECRET"]
def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)

# router = APIRouter(
#     prefix='/client',
#     tags=['client'], dependencies=[Depends(get_token)]
# )

router = APIRouter(
    prefix='/client',
    tags=['client']
)

templates = Jinja2Templates(directory="templates")


@router.get("/appointments")
def appointment(request: Request, token: str = Cookie('token'), db: Session = Depends(get_db)):
    token = jwt.decode(token, secret, algorithms=['HS256'])
    query = db.query(Appointment).all()
    query1 = db.query(Prescription).all()
    id = [token["id"]]
    lst_all = query + query1 + id
  
    try:
        return templates.TemplateResponse('clientside/appointment.html', {
            'request': request,
            'appointment': lst_all
        })
    except Exception as e:
        print(e)

@router.post('/uploadProfile/{id}', status_code=status.HTTP_202_ACCEPTED)
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

    # file_url = "localhost:8000" + generate_name[1:]

    response = RedirectResponse(url='/client/profile', status_code=302)

    return response

@router.post('/{id}', response_model=clientUpdate)
def update(id: str, form_data: clientUpdate = Depends(clientUpdate.as_form), db: Session = Depends(get_db)):
    verify = db.query(Client).filter(Client.cl_id == id).first()
    user_num_cl = db.query(Client).filter(Client.cl_contactNo == form_data.cl_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == form_data.cl_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == form_data.cl_contactNo).first()

    if not verify:
        raise HTTPException(404, 'User to update is not found')
    
    if form_data.cl_contactNo == verify.cl_contactNo:
        user_data = form_data.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
            # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
        db.add(verify)
        db.commit()
        
    else:
        if not user_num_cl: 
            if not user_num_doc: 
                if not user_num_em:
                        user_data = form_data.dict(exclude_unset=True)
                        for key, value in user_data.items():
                            setattr(verify, key, value)
                            # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
                        db.add(verify)
                        db.commit()

                else:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Client. Mobile Number already exists')

    time.sleep(1)

    response = RedirectResponse(url='/client/profile', status_code=302)

    return response

@router.post('/admin/{id}')
def update(id: str, user: clientUpdate, db: Session = Depends(get_db)):
    verify = db.query(Client).filter(Client.cl_id == id).first()
    user_num_cl = db.query(Client).filter(Client.cl_contactNo == user.cl_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == user.cl_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == user.cl_contactNo).first()

    if not verify:
        raise HTTPException(404, 'User to update is not found')

    if user.cl_contactNo == verify.cl_contactNo:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
            # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
        db.add(verify)
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
    response = RedirectResponse(url='/admin/client/', status_code=302)
    return response

@router.get("/about2")
def about(request: Request):
    return templates.TemplateResponse("clientside/about_after_login.html", {"request": request})

@router.get("/home2")
def home(request: Request, db: Session = Depends(get_db)):
    query1 = db.query(Service).all()
    query2 = db.query(Timeslot).all()
    return templates.TemplateResponse('clientside/home_after_login.html', {
        'request': request,
        'services': query1,
        'timeslots': query2
    })  

@router.get("/select_date")
def get_data(request: Request, date: str, db: Session = Depends(get_db)):
    # Retrieve data for the selected date
    query1 = db.query(Service).all()
    query2 = db.query(Timeslot).filter(Timeslot.slot_date == date).all()

    return templates.TemplateResponse('clientside/appointmentModal.html', {
            'request': request,
            'services': query1,
            'timeslots': query2
        })

@router.post('/home3/', response_class=HTMLResponse)
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
    await send_appointment([token["email"]], to_store.ap_clientName, to_store.ap_date, to_store.ap_startTime, to_store.ap_endTime, to_store.ap_service, to_store.ap_amount)
    db.add(to_store)
    db.commit()
    
    time.sleep(1)

    response = RedirectResponse(url='/users/appointments', status_code=302)

    return response

@router.get("/profile")
def profile(request: Request, token: str = Cookie('token'), db: Session = Depends(get_db)):
    query = db.query(Client).all()
    query1 = db.query(Appointment).all()
    query2 = db.query(User_credential).all()
    query3 = db.query(Orders).all()
    token = jwt.decode(token, secret, algorithms=['HS256'])
    id = [token["id"]]
    lst_all = query + query1 + query2 + query3 + id
    try:
        return templates.TemplateResponse('clientside/profile.html', {
                'request': request,
                'profile': lst_all
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
    try:
        return templates.TemplateResponse('clientside/orders.html', {
            'request': request,
            'order_list': lst_all
        })
    except Exception as e:
        print(e)

@router.get('/cancelAppointment/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(Appointment).filter(Appointment.ap_id == id).first()

    currentHour = datetime.datetime.now()
    
    time1 = cancel.ap_startTime

    dt_time1 = datetime.datetime.combine(datetime.date.today(), time1)

    duration = datetime.timedelta(hours=1)

    pastHour = dt_time1

    valid = pastHour - currentHour

    if not cancel:
        raise HTTPException(402, 'Appointment to cancel is not found.')
    elif valid <= duration:
        raise HTTPException(402, 'Cannot cancel appointment 1 hour before your session.')
    else:
        db.query(Appointment).filter(Appointment.ap_id == id).update({'ap_status': "Pending"})
        
    db.commit()

    time.sleep(1)

    response = RedirectResponse(url='/users/appointments', status_code=302)

    return response