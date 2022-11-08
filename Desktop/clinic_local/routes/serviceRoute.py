from xmlrpc.client import Server
from fastapi import APIRouter, Depends, HTTPException, Cookie, status, Response, Request
from sqlalchemy.orm import Session
from schemas.serviceSchema import ServiceBase, ServiceBas
from models.serviceModel import Service
from database import get_db
from dependencies import get_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import time

router = APIRouter(
    prefix='/service',
    tags=['service']
)

templates = Jinja2Templates(directory="templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("clientside/services.html", {"request": request})

@router.get("/admin")
def home(request: Request):
    return templates.TemplateResponse("adminside/adminServices.html", {"request": request})

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
def store(service: ServiceBase, db: Session = Depends(get_db)):

    if db.query(Service).filter(Service.service_name == service.service_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create service. Service already exists')
    else: 
        to_store = Service(
            service_name = service.service_name,
            service_price = service.service_price,
            service_description = service.service_description,
            service_status = "Active"
        )

    db.add(to_store)
    db.commit()
    return {'message': 'Service created successfully.'}

@router.post('/update/{id}', response_model=ServiceBas)
def update(id: str, user: ServiceBas = Depends(ServiceBas.as_form), db: Session = Depends(get_db)):
    verify = db.query(Service).filter(Service.service_id == id).first()

    if not verify:
        raise HTTPException(404, 'Product to update is not found')
    
    # if db.query(Service).filter(Service.service_name == user.service_name).first():
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Service. Service already exists')
    # else:

    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(verify, key, value)
    db.add(verify)
    db.commit()

    time.sleep(1)

    response = RedirectResponse(url='/admin/service', status_code=302)

    return response

@router.post('/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    # deletion = db.query(Product).filter(Product.product_id == id).first()

    if not db.query(Service).filter(Service.service_id == id).update({'service_status': "Inactive"}):
        raise HTTPException(404, 'Service to delete is not found')

    db.commit()
    return {'message': 'Service removed successfully.'}

