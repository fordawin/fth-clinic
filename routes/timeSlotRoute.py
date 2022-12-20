from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from schemas.timeSlotSchema import TimeSlotBase, TimeSlotUpdate
from models.timeSlotModel import Timeslot
from database import get_db
from dependencies import get_token
import datetime as dt
from datetime import timedelta


router = APIRouter(
    prefix='/slot',
    tags=['slot']
)

@router.post('/')
def store(user: TimeSlotBase, db: Session = Depends(get_db)):

    i = 1
    t1 = dt.datetime.strptime('7:00:00', '%H:%M:%S')
    while i < 9:
        time = t1 + timedelta(hours=i)
        to_store = Timeslot(
            slot_capacity = user.slot_capacity,
            slot_time = time,
            slot_date = user.slot_date,
            slot_status = "Active"
        )
        db.add(to_store)
        db.commit()
        i += 1
    return {'message': 'Success successfully.'}

    # service add description
    # appointment add total amount
    # appoitment remove product

    # appointment si user
    # makakapg add service/product si admin
    # makikita ni user yung inadd
    

@router.post('/{id}')
def update(id: str, user: TimeSlotUpdate, db: Session = Depends(get_db)):
    verify = db.query(Timeslot).filter(Timeslot.slot_id == id).first()

    if not verify:
        raise HTTPException(404, 'Timeslot to update is not found')
    
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(verify, key, value)
        db.add(verify)
        db.commit()
        
    return {'message': 'Updated successfully.'} 

@router.post('/deactivate/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(Timeslot).filter(Timeslot.slot_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Time Slot to cancel is not found')
    else:
        db.query(Timeslot).filter(Timeslot.slot_id == id).update({'slot_status': "Inactive"})
        db.commit()
        
   

