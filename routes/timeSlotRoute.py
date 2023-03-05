from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from schemas.timeSlotSchema import TimeSlotBase, TimeSlotUpdate, SlotBase
from models.timeSlotModel import Timeslot
from models.userCredentialModel import User_credential
from database import get_db
from dependencies import get_token, check_employee
from dotenv import dotenv_values
import datetime as dt
import time
from datetime import timedelta
from systemlogs import *

config_credentials = dict(dotenv_values(".env"))
secret = config_credentials["SECRET"]

router = APIRouter(
    prefix='/slot',
    tags=['slot'], dependencies=[Depends(check_employee)]
)

@router.post('/new')
async def store(user: SlotBase, db: Session = Depends(get_db)):

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

    token = jwt.decode(token, secret, algorithms=['HS256'])
    main = db.query(User_credential).filter(User_credential.user_id == token["id"]).first()
    await system_logs("Employee.", main.user_username, f"Created a new timeslots.")
    return {'message': 'Success successfully.'}

@router.post('/{id}')
async def update(id: str, user: TimeSlotUpdate, db: Session = Depends(get_db)):
    verify = db.query(Timeslot).filter(Timeslot.slot_id == id).first()

    if not verify:
        raise HTTPException(404, 'Timeslot to update is not found')
    
    else:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
            db.add(verify)
            db.commit()
        token = jwt.decode(token, secret, algorithms=['HS256'])
        main = db.query(User_credential).filter(User_credential.user_id == token["id"]).first()
        await system_logs("Employee.", main.user_username, f"Updated a timeslot.")
        return {'message': 'Updated successfully.'} 

@router.post('/deactivate/{id}')
async def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(Timeslot).filter(Timeslot.slot_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Time Slot to cancel is not found')
    else:
        token = jwt.decode(token, secret, algorithms=['HS256'])
        main = db.query(User_credential).filter(User_credential.user_id == token["id"]).first()
        await system_logs("Employee.", main.user_username, f"Deactivated a timeslots.")
        db.query(Timeslot).filter(Timeslot.slot_id == id).update({'slot_status': "Inactive"})
        db.commit()
        
   

