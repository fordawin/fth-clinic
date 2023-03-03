from fastapi import APIRouter, Depends, HTTPException, Cookie, status, Response, Request
from sqlalchemy.orm import Session
from schemas.orderSchema import OrderBase, PaymentBase
from models.ordersModel import Orders
from models.userCredentialModel import User_credential
from models.clientModel import Client
from models.productsModel import Product
from database import get_db
from dependencies import get_token, check_employee
from jose import jwt
from systemlogs import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from for_email import *
from dotenv import dotenv_values
router = APIRouter(
    prefix='/orders',
    tags=['orders'], dependencies=[Depends(get_token)]
)

config_credentials = dict(dotenv_values(".env"))

secret = config_credentials["SECRET"]
templates = Jinja2Templates(directory="templates")

@router.post('/')
async def store(orders: OrderBase, token: str = Cookie('token'),db: Session = Depends(get_db)):
    token = jwt.decode(token, secret, algorithms=['HS256'])
    price = db.query(Product).filter(Product.product_id == orders.order_productid).first()

    if not price:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Product does not exist')
    else:
        user = db.query(Client).filter(Client.cl_user_credential == token["id"]).first()

        main = db.query(User_credential).filter(User_credential.user_id == token["id"]).first()

        count = price.product_quantity - orders.order_quantity

        total = (price.product_price * orders.order_quantity) - (orders.order_quantity * int(price.product_discount))

        db.query(Product).filter(Product.product_id == orders.order_productid).update({'product_quantity': count}) 
        to_store = Orders(
            order_quantity = orders.order_quantity,
            order_total = total,
            order_productid = orders.order_productid,
            order_user = user.cl_firstName + " " + user.cl_middleName + " " + user.cl_lastName,
            order_userid = token["id"],
            order_remarks = price.product_name
        )
        await system_logs(main.user_username, "Placed an Order.")
    db.add(to_store)
    db.commit()
    
    return {'message': "Order Placed"}
    
