from fastapi import APIRouter, Depends, HTTPException, Cookie, status, Request, Response
from dotenv import dotenv_values
from sqlalchemy.orm import Session
from schemas.userCredentialSchema import LoginForm, TokenData
from models.userCredentialModel import User_credential
from models.productsModel import Product
from schemas.paymentSchema import PaymentBase, PaymentUpdate
from models.paymentModel import Payment
from models.serviceModel import Service
from models.timeSlotModel import Timeslot
from models.clientModel import Client
from models.ordersModel import Orders
from models.appointmentModel import Appointment
from database import get_db
from dependencies import get_token, check_employee
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from passlib.context import CryptContext
from jose import jwt
import time
from for_email import *

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

config_credentials = dict(dotenv_values(".env"))

secret = config_credentials["SECRET"]
def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)

router = APIRouter(
    prefix='/payment',
    tags=['payment'], dependencies=[Depends(check_employee)]
)

templates = Jinja2Templates(directory="templates")

@router.get('/')
def employee(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse('employeeside/employeeDashboard.html', {
        'request': request,
    })

@router.get('/base')
def appointments(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Appointment).all()
        query1 = db.query(Service).all()
        query2 = db.query(Timeslot).all()
        query3 = db.query(User_credential).all()
        query4 = db.query(Client).all()
        applen = int(len(query))
        serlen = int(len(query1))
        clilen = int(len(query3))
        namlen = int(len(query4))
        serlist = [(serlen)]
        applist = [(applen)]
        clilist = [(clilen)]
        namlist = [(namlen)]
        timlen = int(len(query2))
        timlist = [(timlen)]
        lst_all = query + query1 + query2 + query3 + query4 + applist + serlist + clilist + namlist + timlist
        return templates.TemplateResponse('employeeside/employeePayment.html', {
            'request': request,
            'appointments': lst_all,
            'services': query1,
            'timeslots': query2,
            'usercreds': query3,
            'clients': query4
        })
        
    except Exception as e:
        print(e)

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
        lst_all = query + query1 + query2 + applist + serlist + timlist
        return templates.TemplateResponse('employeeside/employeePaymentDone.html', {
            'request': request,
            'appointments': lst_all
        })
        
    except Exception as e:
        print(e)

@router.post('/base')
def store(form_data: PaymentBase, db: Session = Depends(get_db)):

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

@router.get('/pending')
def employee(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Orders).all()
        return templates.TemplateResponse('employeeside/employeeOrderPending.html', {
            'request': request,
            'order_list': query
        })
        
    except Exception as e:
        print(e)

@router.get('/accepted')
def employee(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Orders).all()
        return templates.TemplateResponse('employeeside/employeeOrderAccepted.html', {
            'request': request,
            'order_list': query
        })
        
    except Exception as e:
        print(e)

@router.get('/cancelled')
def employee(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Orders).all()
        return templates.TemplateResponse('employeeside/employeeOrderCancelled.html', {
            'request': request,
            'order_list': query
        })
        
    except Exception as e:
        print(e)

@router.post('/{id}', response_model=PaymentUpdate)
def update(id: str, user: PaymentUpdate, db: Session = Depends(get_db)):
    verify = db.query(Payment).filter(Payment.payment_id == id).first()

    if not verify:
        raise HTTPException(404, 'Payment to update is not found')
    
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(verify, key, value)
        db.add(verify)
        db.commit()
        
    return {'message': 'Appointment updated successfully.'} 

@router.post('/deactivate/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(Payment).filter(Payment.payment_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Payment to cancel is not found')
    else:
        db.query(Payment).filter(Payment.payment_id == id).update({'payment_status': "Canceled"})
        
    db.commit()

@router.get('/accept/{id}')
async def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(Orders).filter(Orders.order_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Order to cancel is not found')
    else:
        db.query(Orders).filter(Orders.order_id == id).update({'order_status': "For Pick-up"})

    db.commit()

    users = db.query(User_credential).filter(User_credential.user_id == cancel.order_userid).first()

    print(users)

    await for_pickup([users.user_email])

    time.sleep(1)

    response = RedirectResponse(url='/payment/pending', status_code=302)

    return response

@router.get('/deny/{id}')
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

    response = RedirectResponse(url='/payment/pending', status_code=302)

    return response

@router.get('/products', response_class=HTMLResponse)
def products(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Product).all()
        return templates.TemplateResponse('employeeside/employeeProducts.html', {
            'request': request,
            'product': query
        })

    except Exception as e:
        print(e)

@router.get('/services', response_class=HTMLResponse)
def services(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Service).all()
        return templates.TemplateResponse('employeeside/employeeServices.html', {
            'request': request,
            'service': query
        })

    except Exception as e:
        print(e)

@router.get('/logout')
def logout(response: Response):
    response = RedirectResponse(url='/users/login', status_code=307)
    response.delete_cookie('token')
    response.delete_cookie('type')
    return response

     