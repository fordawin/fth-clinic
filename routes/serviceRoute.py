from xmlrpc.client import Server
from fastapi import APIRouter, Depends, HTTPException, Cookie, status, Response, Request
from sqlalchemy.orm import Session
from schemas.serviceSchema import ServiceBase, ServiceBas, updateService
from models.serviceModel import Service
from models.userCredentialModel import User_credential
from dotenv import dotenv_values
from database import get_db
from dependencies import get_token, check_employee
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import time
from systemlogs import *

config_credentials = dict(dotenv_values(".env"))
secret = config_credentials["SECRET"]
router = APIRouter(
    prefix='/service',
    tags=['service'], dependencies=[Depends(check_employee)]
)

templates = Jinja2Templates(directory="templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("clientside/services.html", {"request": request})

@router.get('/')
def all(db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.service_status == "Active").all()
    return {'Service': service}

@router.get('/{id}')
def read(id: str, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.service_id == id).first()
    if not service:
        raise HTTPException(404, 'Service not found')
    return {'Service': service}

@router.post('/')
async def store(service: ServiceBase, db: Session = Depends(get_db)):

    if db.query(Service).filter(Service.service_name == service.service_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create service. Service already exists')
    else: 
        to_store = Service(
            service_name = service.service_name,
            service_price = service.service_price,
            service_description = service.service_description,
            service_status = "Active"
        )
    token = jwt.decode(token, secret, algorithms=['HS256'])
    main = db.query(User_credential).filter(User_credential.user_id == token["id"]).first()
    await system_logs("Employee.", main.user_username, f"Created a new service.")


    db.add(to_store)
    db.commit()
    return {'message': 'Service created successfully.'}

@router.post('/update/{id}')
async def update(id: str, user: updateService, db: Session = Depends(get_db)):
    verify = db.query(Service).filter(Service.service_id == id).first()

    if not verify:
        raise HTTPException(404, 'Service to update is not found')
    else:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
        token = jwt.decode(token, secret, algorithms=['HS256'])
        main = db.query(User_credential).filter(User_credential.user_id == token["id"]).first()
        await system_logs("Employee.", main.user_username, f"Updated a service.")
        db.add(verify)
        db.commit()

@router.post('/{id}')
async def deactivate(id: str, db: Session = Depends(get_db)):

    if not db.query(Service).filter(Service.service_id == id).update({'service_status': "Inactive"}):
        raise HTTPException(404, 'Service to delete is not found')
    token = jwt.decode(token, secret, algorithms=['HS256'])
    main = db.query(User_credential).filter(User_credential.user_id == token["id"]).first()
    await system_logs("Employee.", main.user_username, f"Deactivated a service.")

    db.commit()
    return {'message': 'Service removed successfully.'}

