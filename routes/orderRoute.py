from fastapi import APIRouter, Depends, HTTPException, Cookie, status, Response, Request
from sqlalchemy.orm import Session
from schemas.orderSchema import OrderBase, PaymentBase
from models.ordersModel import Orders
from models.clientModel import Client
from models.productsModel import Product
from database import get_db
from dependencies import get_token
from jose import jwt
import time
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix='/orders',
    tags=['orders'], dependencies=[Depends(get_token)]
)

secret = 'a very shady secret'
templates = Jinja2Templates(directory="templates")

# @router.get("/")
# def home(request: Request):
#     return templates.TemplateResponse("adminside/adminProducts.html", {"request": request})

@router.get('/')
def all(db: Session = Depends(get_db)):
    orders = db.query(Orders).filter(orders.order_status == "Active").all()
    return {'Orders': orders}

@router.get('/{id}')
def read(id: str, db: Session = Depends(get_db)):
    orders = db.query(Orders).filter(Orders.order_id == id).first()
    if not orders:
        raise HTTPException(404, 'Order not found')
    return {'Orders': orders}

@router.post('/')
def store(orders: OrderBase, token: str = Cookie('token'),db: Session = Depends(get_db)):
    token = jwt.decode(token, secret, algorithms=['HS256'])
    price = db.query(Product).filter(Product.product_id == orders.order_productid).first()

    if not price:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Product does not exist')
    else:
        user = db.query(Client).filter(Client.cl_user_credential == token["id"]).first()

        count = price.product_quantity - orders.order_quantity

        total = price.product_price * orders.order_quantity

        db.query(Product).filter(Product.product_id == orders.order_productid).update({'product_quantity': count}) 
        to_store = Orders(
            order_quantity = orders.order_quantity,
            order_total = total,
            order_productid = orders.order_productid,
            order_user = user.cl_firstName + " " + user.cl_middleName + " " +user.cl_lastName,
            order_userid = token["id"],
            order_remarks = price.product_name
        )

    db.add(to_store)
    db.commit()
    return {'message': "Order Placed"}

# @router.post('/{id}', response_model=productUpdate)
# def update(id: str, user: productUpdate, db: Session = Depends(get_db)):
#     verify = db.query(Product).filter(Product.product_id == id).first()

#     if not verify:
#         raise HTTPException(404, 'Product to update is not found')
    
#     if db.query(Product).filter(Product.product_name == user.product_name).first():
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Product. Product already exists')
#     else:
#         user_data = user.dict(exclude_unset=True)
#         for key, value in user_data.items():
#             setattr(verify, key, value)
#         db.add(verify)
#         db.commit()

#         return {'message': 'Product updated successfully.'} 
    
@router.post('/{id}')
def pickup(id: str, db: Session = Depends(get_db)):
    # deletion = db.query(Product).filter(Product.product_id == id).first()

    if not db.query(Orders).filter(Orders.order_id == id).update({'order_status': "For Pickup"}):
        raise HTTPException(404, 'Order to pickup is not found')

    db.commit()
    return {'message': 'Success.'}

@router.post('/payment/{id}')
def payment(id: str, pay: PaymentBase = Depends(PaymentBase.as_form), db: Session = Depends(get_db)):
    payment = db.query(Orders).filter(Orders.order_id == id).first()

    if pay.order_payment == payment.order_total:
        db.query(Orders).filter(Orders.order_id == id).update({'order_status': "Paid"})
        db.commit()

        time.sleep(1)

        response = RedirectResponse(url='/payment/accepted', status_code=302)

        return response

    else:
        raise HTTPException(404, 'Insufficient Payment')
