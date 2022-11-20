from click import File
from fastapi import APIRouter, Depends, HTTPException, Cookie, UploadFile, status, Response, Request
from sqlalchemy.orm import Session
from schemas.productSchema import ProductBase, productUpdate
from models.productsModel import Product
from database import get_db
from dependencies import get_token
from fastapi.templating import Jinja2Templates

#img
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image
import secrets


router = APIRouter(
    prefix='/product',
    tags=['product']
) 

templates = Jinja2Templates(directory="templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("adminside/adminProducts.html", {"request": request})

@router.get('/')
def all(db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_status == "Active").all()
    return {'Product': product}

@router.get('/{id}')
def read(id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == id).first()
    if not product:
        raise HTTPException(404, 'Product not found')
    return {'Product': product}

@router.post('/')
async def store(request: Request, product: ProductBase = Depends(ProductBase.as_form), file: UploadFile = File(...), db: Session = Depends(get_db)):

    if db.query(Product).filter(Product.product_name == product.product_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot create product. Product already exists')
    else: 
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

        product_pic = token_name

        # file_url = "localhost:8000" + generate_name[1:]
        to_store = Product(
            product_name = product.product_name,
            product_pic = product_pic,
            product_price = product.product_price,
            product_quantity = product.product_quantity,
            product_description = product.product_description,
            product_status = "Active"
        )

        db.add(to_store)
        db.commit()
        return {'message': 'Product created successfully.'}

@router.post('/{id}', response_model=productUpdate)
def update(id: str, user: productUpdate, db: Session = Depends(get_db)):
    verify = db.query(Product).filter(Product.product_id == id).first()

    if not verify:
        raise HTTPException(404, 'Product to update is not found')
    
    if db.query(Product).filter(Product.product_name == user.product_name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Product. Product already exists')
    else:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
        db.add(verify)
        db.commit()

        return {'message': 'Product updated successfully.'} 
    
@router.post('/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    # deletion = db.query(Product).filter(Product.product_id == id).first()

    if not db.query(Product).filter(Product.product_id == id).update({'product_status': "Inactive"}):
        raise HTTPException(404, 'Product to delete is not found')

    db.commit()
    return {'message': 'Product removed successfully.'}

