from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from routes import authRoutes, clientRoute, userCredentialRoutes, doctorRoute, employeeRoute, productRoute, serviceRoute, adminRoutes, timeSlotRoute, appointmentRoute, prescriptionRoute, receiptRoute, paymentRoute, userRoutes, orderRoute
from database import get_db, engine
from models.timeSlotModel import Timeslot
from dependencies import get_token
import models
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

models.paymentModel.Base.metadata.create_all(bind=engine)

async def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse('auth.html', {'request': request}, status_code=404)
async def method_not_allowed(request: Request, exc: HTTPException):
    return templates.TemplateResponse('auth.html', {'request': request}, status_code=405)
# async def unauthorized(request: Request, exc: HTTPException):
#     return templates.TemplateResponse('auth.html', {'request': request}, status_code=401)

# Register template folder
templates = Jinja2Templates('templates')

exception_handlers = {404: not_found_error,
                      405: method_not_allowed}

# app = FastAPI()
app = FastAPI(exception_handlers=exception_handlers)
# Mount static folder
app.mount('/static', StaticFiles(directory='static'), name='static')

# Register Routes
app.include_router(userCredentialRoutes.router)
app.include_router(clientRoute.router)
app.include_router(doctorRoute.router)
app.include_router(employeeRoute.router)
app.include_router(productRoute.router)
app.include_router(serviceRoute.router)
app.include_router(adminRoutes.router)
app.include_router(timeSlotRoute.router)
app.include_router(appointmentRoute.router)
app.include_router(prescriptionRoute.router)
app.include_router(receiptRoute.router)
app.include_router(paymentRoute.router)
app.include_router(userRoutes.router)
app.include_router(authRoutes.router)
app.include_router(orderRoute.router)

@app.get('/', response_class=HTMLResponse)
def index():
    return RedirectResponse(url='/users', status_code=302)


@app.get("/logged")
def logged(request: Request):
    return templates.TemplateResponse("/logged.html", {"request": request}) 

