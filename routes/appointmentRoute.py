from fastapi import APIRouter, Depends, HTTPException, Cookie, status, Request
from sqlalchemy.orm import Session, joinedload
from schemas.appointmentSchema import AppointmentBase, AppointmentUpdate, AppointmentEmployee
from models.appointmentModel import Appointment
from models.timeSlotModel import Timeslot
from schemas.serviceSchema import ServiceBase
from models.serviceModel import Service
from models.clientModel import Client
from dotenv import dotenv_values
from database import get_db
from dependencies import get_token
from jose import jwt
import datetime as dt
from datetime import timedelta
import random
import string
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
import time
from for_email import *
from systemlogs import *
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
router = APIRouter(
    prefix='/appointment',
    tags=['appointment'], dependencies=[Depends(get_token)]
)

templates = Jinja2Templates(directory="templates")

@router.get('/')
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

        lst_all = query + query1 + query2 + applist + serlist + timlist

        return templates.TemplateResponse('adminside/adminAppointments.html', {
            'request': request,
            'appointments': lst_all
        })
        
    except Exception as e:
        print(e)

@router.post('/', response_class=HTMLResponse)
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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot schedule appointment. Reached maximum capacity')

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
    await send_appointment([token["email"]], to_store.ap_clientName, to_store.ap_date, to_store.ap_startTime, to_store.ap_endTime, to_store.ap_service, to_store.ap_amount)
    db.add(to_store)
    
    db.commit()
    time.sleep(1)

    response = RedirectResponse(url='/appointment', status_code=302)

    return response

@router.post('/{id}')
def update(id: str, user: AppointmentUpdate, db: Session = Depends(get_db)):
    verify = db.query(Appointment).filter(Appointment.ap_id == id).first()

    limit = db.query(Timeslot).filter(Timeslot.slot_id == verify.ap_slotID).first()

    sched = db.query(Appointment).filter(Appointment.ap_slotID == limit.ap_slotID).all()

    bilang = int(len(sched))

    kumpara = int(limit.slot_capacity)

    if not verify:
        raise HTTPException(404, 'Appointment to update is not found')
    
    if bilang > kumpara-1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot schedule Appointment. Reached maximum capacity')
    
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(verify, key, value)
        db.add(verify)
        db.commit()
        
    return {'message': 'Appointment updated successfully.'} 

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

    response = RedirectResponse(url='/users/appointments', status_code=302)

    return response

@router.post('/employee', response_class=HTMLResponse)
async def store(form_data: AppointmentEmployee = Depends(AppointmentEmployee.as_form), db: Session = Depends(get_db)):

    serbisyo = db.query(Service).filter(Service.service_id == form_data.ap_serviceType).first()

    oras = db.query(Timeslot).filter(Timeslot.slot_id == form_data.ap_slotID).first()

    cliente = db.query(Client).filter(Client.cl_user_credential == form_data.ap_clientID).first()

    simula = oras.slot_time

    umpisa = dt.datetime.strptime(f'{simula}', '%H:%M')
    
    hangganan = umpisa + timedelta(hours=1)

    sched = db.query(Appointment).filter(Appointment.ap_slotID == form_data.ap_slotID).all()

    bilang = int(len(sched))

    kumpara = int(oras.slot_capacity)

    if bilang > kumpara-1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot schedule appointment. Reached maximum capacity')

    to_store = Appointment(
        ap_number = randoms(),
        ap_clientID = form_data.ap_clientID,
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
    await send_appointment([cliente.user_email], to_store.ap_clientName, to_store.ap_date, to_store.ap_startTime, to_store.ap_endTime, to_store.ap_service, to_store.ap_amount)
    db.add(to_store)
    db.commit()
    

    time.sleep(1)

    response = RedirectResponse(url='/payment/base', status_code=302)

