from fastapi import APIRouter, Depends, HTTPException, Cookie, Request, Response, status
from dotenv import dotenv_values
from sqlalchemy.orm import Session
from models.doctorModel import Doctor
from models.clientModel import Client
from models.employeeModel import Employee
from schemas.doctorSchema import doctorUpdate
from schemas.prescriptionSchema import PrescriptionBase, PrescriptionUpdate
from schemas.userCredentialSchema import LoginForm, TokenData
from models.userCredentialModel import User_credential
from models.prescriptionModel import Prescription
from models.appointmentModel import Appointment
from models.serviceModel import Service
from models.timeSlotModel import Timeslot
from database import get_db
from dependencies import get_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from passlib.context import CryptContext
from jose import jwt
import time

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

config_credentials = dict(dotenv_values(".env"))

secret = config_credentials["SECRET"]
def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)

router = APIRouter(
    prefix='/prescription',
    tags=['prescription']
)

templates = Jinja2Templates(directory="templates")

@router.get('/')
def employee(request: Request):
    return templates.TemplateResponse('doctorside/doctorDashboard.html', {
        'request': request,
    })

@router.get('/profile')
def employee(request: Request, token: str = Cookie('token'), db: Session = Depends(get_db)):
    query = db.query(Doctor).all()
    token = jwt.decode(token, secret, algorithms=['HS256'])
    id = [token["id"]]
    lst_all = query + id
    try:
        return templates.TemplateResponse('doctorside/profile.html', {
            'request': request,
            'doctor': lst_all
        })
    except Exception as e:
        print(e)

@router.get('/login')
def employee(request: Request):
    return templates.TemplateResponse('doctorside/login.html', {
        'request': request,
    })
    
@router.post('/login', response_class=HTMLResponse)
async def verify(response: Response, form_data: LoginForm = Depends(LoginForm.as_form), db: Session = Depends(get_db)):
    try:
        user = db.query(User_credential).filter(User_credential.user_email == form_data.user_email).first()
        if user:
            match = password_verify(form_data.user_password, user.user_password)
            if match:
                data = TokenData(id = user.user_id, email = user.user_email, type = user.user_type)
                token = jwt.encode(dict(data), secret)
                response = RedirectResponse(url='/prescription/base', status_code=302)
                response.set_cookie('token', token, httponly=True)

                return response
                
    except Exception as e:
        print(e)

@router.get('/base')
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
        return templates.TemplateResponse('doctorside/doctorPrescription.html', {
            'request': request,
            'appointments': lst_all
        })
        
    except Exception as e:
        print(e)

@router.post('/base')
def store(form_data: PrescriptionBase, db: Session = Depends(get_db)):

    db.query(Appointment).filter(Appointment.ap_id == form_data.presc_appointmentID).update({"ap_type": "Done"})

    to_store = Prescription(
        presc_appointmentID = form_data.presc_appointmentID,
        presc_medication = form_data.presc_medication,
        presc_treatment = form_data.presc_treatment,
        presc_remarks = form_data.presc_remarks
    )
    db.add(to_store)
    db.commit()
    
    # time.sleep(1)

    # response = RedirectResponse(url='/prescription/base', status_code=302)

    return

@router.get('/done')
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
        return templates.TemplateResponse('doctorside/doctorPrescriptionDone.html', {
            'request': request,
            'appointments': lst_all
        })
        
    except Exception as e:
        print(e)

@router.post('/{id}', response_model=PrescriptionUpdate)
def update(id: str, user: PrescriptionUpdate, db: Session = Depends(get_db)):
    verify = db.query(Prescription).filter(Prescription.presc_id == id).first()

    if not verify:
        raise HTTPException(404, 'Prescription to update is not found')
    
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(verify, key, value)
        db.add(verify)
        db.commit()
        
    return {'message': 'Updated successfully.'} 

@router.post('/update/{id}', response_model=doctorUpdate)
def update(id: str, user: doctorUpdate = Depends(doctorUpdate.as_form), db: Session = Depends(get_db)):
    verify = db.query(Doctor).filter(Doctor.dt_id == id).first()
    user_num_cl = db.query(Client).filter(Client.cl_contactNo == user.dt_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == user.dt_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == user.dt_contactNo).first()

    if not verify:
        raise HTTPException(404, 'User to update is not found')

    if user.dt_contactNo == verify.dt_contactNo:
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

                        return {'message': 'Doctor updated successfully.'} 
                else:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Doctor. Mobile Number already exists')
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Doctor. Mobile Number already exists')
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Doctor. Mobile Number already exists')
    
    time.sleep(1)

    response = RedirectResponse(url='/prescription/profile', status_code=302)

    return response

@router.get('/logout')
def logout(response: Response):
    response = RedirectResponse(url='/users/login', status_code=307)
    response.delete_cookie('token')
    response.delete_cookie('type')
    return response