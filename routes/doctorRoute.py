from fastapi import APIRouter, Depends, HTTPException, Cookie, status, Response, Request
from sqlalchemy.orm import Session
from schemas.doctorSchema import doctorUpdate
from models.userCredentialModel import User_credential
from models.clientModel import Client
from models.doctorModel import Doctor
from models.employeeModel import Employee
from models.appointmentModel import Appointment
from models.timeSlotModel import Timeslot
from for_email import *
from database import get_db
from dependencies import get_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import time
from systemlogs import *
#image upload
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image
import secrets


router = APIRouter(
    prefix='/doctor',
    tags=['doctor']
)

templates = Jinja2Templates(directory="templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("adminside/adminDoctor.html", {"request": request})

@router.post('/{id}')
async def update(id: str, user: doctorUpdate, db: Session = Depends(get_db)):
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

        await system_logs("Dr.", verify.dt_fullName, f"Updated their profile.") 
        db.add(verify)
        
        db.commit()
        
    else:
        if not user_num_cl: 
            if not user_num_doc: 
                if not user_num_em:
                        user_data = user.dict(exclude_unset=True)
                        for key, value in user_data.items():
                            setattr(verify, key, value)
                        
                        await system_logs("Dr.", verify.dt_fullName, f"Updated their profile.") 
                        db.add(verify)
                        db.commit()

                        return {'message': 'Doctor updated successfully.'} 
                else:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Doctor. Mobile Number already exists')
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Doctor. Mobile Number already exists')
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Doctor. Mobile Number already exists')

@router.post('/uploadProfile/{id}', status_code=status.HTTP_202_ACCEPTED)
async def upload_profile(id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    verify = db.query(Doctor).filter(Doctor.dt_id == id).first()

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

    verify.dt_pic = token_name
    db.add(verify)
    db.commit()

    file_url = "localhost:8000" + generate_name[1:]
    return {"status": "ok", "filename": file_url}

@router.get('/deactivate/{id}')
async def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Doctor to delete is not found')
    else:
        await system_logs("Dr.", cancel.user_username, f"'s account has been deactivated'") 
        db.query(User_credential).filter(User_credential.user_id == id).update({'user_status': "Inactive"})
        
    db.commit()
    
    time.sleep(1)  
    response = RedirectResponse(url='/admin/doctor/', status_code=302)
    return response

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
    await system_logs("Dr.", users.user_username, f"Approved the cancellation of appointment.") 
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
    await system_logs("Dr.", users.user_username, f"Denied the cancellation of appointment.") 
    db.commit()

    return