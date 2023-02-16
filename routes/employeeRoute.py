from fastapi import APIRouter, Depends, HTTPException, Cookie, status, Response, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
from schemas.employeeSchema import employeeUpdate
from schemas.userCredentialSchema import UserBase, EmployeeBase
from models.userCredentialModel import User_credential
from models.clientModel import Client
from models.doctorModel import Doctor
from models.employeeModel import Employee
from database import get_db
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import time
from jose import jwt
from for_email import *
from datatables import DataTable

#image upload
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image
import secrets


from dotenv import dotenv_values
config_credentials = dict(dotenv_values(".env"))

secret = config_credentials["SECRET"]


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def password_verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def password_hash(password):
    return pwd_context.hash(password)

router = APIRouter(
    prefix='/employee',
    tags=['employee']
)

templates = Jinja2Templates(directory="templates")

@router.get('/', response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    try:
        employee = db.query(Employee).all()
        return templates.TemplateResponse('adminside/adminEmployee.html', {
            'request': request,
            'employees': employee
        })
    except Exception as e:
        print(e)


@router.get('/all')
def findAll(db: Session = Depends(get_db), token: str = Cookie('token')):
    users = db.query(Employee).filter(Employee.em_status == "Active").all()

    # token = jwt.decode(token, secret, algorithms=['HS256'])

    return {'users': users}

@router.get('/{id}', status_code=status.HTTP_202_ACCEPTED)
def findOne(id: str, db: Session = Depends(get_db)):

    user = db.query(Employee).filter(Employee.em_id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Employee does not exists')

    return {'user': user}

@router.post('/{id}')
def update(id: str, user: employeeUpdate, db: Session = Depends(get_db)):
    verify = db.query(Employee).filter(Employee.em_id == id).first()
    user_num_cl = db.query(Client).filter(Client.cl_contactNo == user.em_contactNo).first()
    user_num_doc = db.query(Doctor).filter(Doctor.dt_contactNo == user.em_contactNo).first()
    user_num_em = db.query(Employee).filter(Employee.em_contactNo == user.em_contactNo).first()

    if not verify:
        raise HTTPException(404, 'User to update is not found')

    if user.em_contactNo == verify.em_contactNo:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(verify, key, value)
            # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
        db.add(verify)
        db.commit()
    else:
        if not user_num_cl: 
            if not user_num_doc: 
                if not user_num_em:
                        user_data = user.dict(exclude_unset=True)
                        for key, value in user_data.items():
                            setattr(verify, key, value)
                            # db.query(User_credential).filter(User_credential.user_id == id).update(verify)
                        db.add(verify)
                        db.commit()

                        return {'message': 'Employee updated successfully.'} 
                else:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Employee. Mobile Number already exists')
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Employee. Mobile Number already exists')
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'Cannot update Employee. Mobile Number already exists')

@router.post('/home')
async def createEmployee(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    address = form.get("address")
    email = form.get("email")
    contact = form.get("contact")
    to_store = User_credential(
        user_username = name,
        user_password = password_hash(address),
        user_email = email,
        user_type = "Employee"   
    )
    db.add(to_store)
    db.commit()
    db.refresh(to_store)   
    # to_employee = Employee(
    #     em_pic = "ASD",
    #     em_firstName = name,
    #     em_middleName = employee.em_middleName,
    #     em_lastName = employee.em_lastName,
    #     em_fullName = employee.em_firstName + " " + employee.em_middleName + " " + employee.em_lastName,
    #     em_houseNo = address,
    #     em_street = employee.em_street,
    #     em_brgy = employee.em_brgy,
    #     em_city = employee.em_city,
    #     em_address = employee.em_houseNo + " " + employee.em_street + " " + employee.em_brgy + " " + employee.em_city,
    #     em_status = "Active",
    #     em_contactNo = contact,
    #     em_user_credential = to_store.user_id,
    #     # cl_created_by = client.cl_created_by,
    #     # cl_updated_by = client.cl_updated_by
    # )
    # db.add(to_employee)
    # db.commit()
    # db.refresh(to_employee)

    return {"Employee Successfully Registered"}

@router.put('/approval/{id}')
async def approval(id: str, db: Session = Depends(get_db)):
    approval = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not approval:
        raise HTTPException(404, 'User not found')
    else:
        db.query(User_credential).filter(User_credential.user_id == id).update({'user_status': "Active"})
   
        db.query(Client).filter(Client.cl_user_credential == id).update({'cl_status': "Active"})

        
    db.commit()

    return {'message': 'User approved successfully.'}

@router.put('/decline/{id}')
async def decline(id: str, db: Session = Depends(get_db)):
    approval = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not approval:
        raise HTTPException(404, 'User not found')
    else:
        db.query(User_credential).filter(User_credential.user_id == id).update({'user_status': "Declined"})
   
        db.query(Client).filter(Client.cl_user_credential == id).update({'cl_status': "Declined"})

    db.commit()
    
    return {'message': 'User denied successfully.'}

@router.get('/datatable')
def datatable(request: Request, db: Session = Depends(get_db)):
    try:
        def perform_search(queryset, user_input):
            return queryset.filter(
                or_(
                    Employee.em_id.like('%' + user_input + '%'),
                    Employee.em_firstName.like('%' + user_input + '%'),
                    Employee.em_address.like('%' + user_input + '%')
                )
            )
    
        table = DataTable(dict(request.query_params), Employee, db.query(Employee), [
            'em_id',
            'em_firstName',
            'em_adress'
        ])

        table.searchable(lambda queryset, user_input: perform_search(queryset, user_input))
    
        return table.json()
    except Exception as e:
        print(e)
                    
@router.post('/uploadProfile/{id}', status_code=status.HTTP_202_ACCEPTED)
async def upload_profile(id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    verify = db.query(Employee).filter(Employee.em_id == id).first()

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

    verify.em_pic = token_name
    db.add(verify)
    db.commit()

    file_url = "localhost:8000" + generate_name[1:]
    return {"status": "ok", "filename": file_url}

@router.get('/deactivate/{id}')
def deactivate(id: str, db: Session = Depends(get_db)):
    cancel = db.query(User_credential).filter(User_credential.user_id == id).first()

    if not cancel:
        raise HTTPException(404, 'Employee to cancel is not found')
    else:
        db.query(User_credential).filter(User_credential.user_id == id).update({'user_status': "Inactive"})
        
    db.commit()
    
    time.sleep(1)  
    response = RedirectResponse(url='/admin/employee/', status_code=302)
    return response