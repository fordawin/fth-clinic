from click import File
from fastapi import APIRouter, Depends, HTTPException, Cookie, UploadFile, status, Response, Request
from sqlalchemy.orm import Session
from schemas.productSchema import ProductBase, productUpdate, Discount
from models.productsModel import Product
from database import get_db
from dotenv import dotenv_values
from dependencies import get_token, check_employee
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from models.userCredentialModel import User_credential
import time
from systemlogs import *
#img
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image
import secrets

config_credentials = dict(dotenv_values(".env"))
secret = config_credentials["SECRET"]
router = APIRouter(
    prefix='/product',
    tags=['product'], dependencies=[Depends(check_employee)]
) 

templates = Jinja2Templates(directory="templates")

@router.get('/products', response_class=HTMLResponse)
def products(request: Request, db: Session = Depends(get_db)):
    try:
        query = db.query(Product).all()
        return templates.TemplateResponse('employeeside/employeeBase.html', {
            'request': request,
            'product': query
        })

    except Exception as e:
        print(e)

@router.post('/default')
async def store(request: Request, product: ProductBase = Depends(ProductBase.as_form), file: UploadFile = File(...), db: Session = Depends(get_db)):

    if db.query(Product).filter(Product.product_name == product.product_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create product. Product already exists')
    else: 
        FILEPATH = "static/images/"
        filename = file.filename
        extension = filename.split(".")[1]

        if extension not in ["png", "jpg", "PNG", "jpeg", "JPG", "JPEG"]:
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

        product_pic = token_name

        # file_url = "localhost:8000" + generate_name[1:]
        to_store = Product(
            product_name = product.product_name,
            product_pic = product_pic,
            product_price = product.product_price,
            product_quantity = product.product_quantity,
            product_discount = 0,
            product_type = "Default",
            product_description = product.product_description,
            product_status = "Active"
        )
        token = jwt.decode(token, secret, algorithms=['HS256'])
        main = db.query(User_credential).filter(User_credential.user_id == token["id"]).first()
        await system_logs("Employee.", main.user_username, f"Created a new product.")

        db.add(to_store)
        db.commit()

        response = RedirectResponse(url='/payment/products', status_code=302)

        return response

@router.post('/promo')
async def store(request: Request, product: ProductBase = Depends(ProductBase.as_form), file: UploadFile = File(...), db: Session = Depends(get_db)):

    if db.query(Product).filter(Product.product_name == product.product_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create product. Product already exists')
    else: 
        FILEPATH = "static/images/"
        filename = file.filename
        extension = filename.split(".")[1]

        if extension not in ["png", "jpg", "PNG", "jpeg", "JPG", "JPEG"]:
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

        product_pic = token_name

        # file_url = "localhost:8000" + generate_name[1:]
        to_store = Product(
            product_name = product.product_name,
            product_pic = product_pic,
            product_price = product.product_price,
            product_quantity = product.product_quantity,
            product_discount = 0,
            product_type = "Promo",
            product_description = product.product_description,
            product_status = "Active"
        )

        db.add(to_store)
        db.commit()

        response = RedirectResponse(url='/payment/products', status_code=302)

        return response

@router.post('/{id}', response_model=productUpdate)
async def update(id: str, user: productUpdate, db: Session = Depends(get_db)):
    verify = db.query(Product).filter(Product.product_id == id).first()

    if not verify:
        raise HTTPException(404, 'Product to update is not found')
    
    if db.query(Product).filter(Product.product_name == user.product_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Product. Product already exists')
    else:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
        token = jwt.decode(token, secret, algorithms=['HS256'])
        main = db.query(User_credential).filter(User_credential.user_id == token["id"]).first()
        await system_logs("Employee.", main.user_username, f"Updated a product.")

        db.add(verify)
        db.commit()

        return {'message': 'Product updated successfully.'} 
    
@router.get('/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    # deletion = db.query(Product).filter(Product.product_id == id).first()

    if not db.query(Product).filter(Product.product_id == id).update({'product_status': "Inactive"}):
        raise HTTPException(404, 'Product to delete is not found')

    db.commit()

    time.sleep(1)
    
    response = RedirectResponse(url='/payment/products/', status_code=302)

    return response

@router.post('/discount/{id}')
def discount(id: str, product: Discount, db: Session = Depends(get_db)):

    if not db.query(Product).filter(Product.product_id == id).update({'product_discount': product.product_discount}):
        raise HTTPException(404, 'Product not found')

    db.commit()
    db.expire_all()
    return {'message': 'Discount successfully placed.'}


