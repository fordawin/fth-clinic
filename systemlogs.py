from fastapi import (BackgroundTasks, UploadFile, 
                    File, Form, Depends, HTTPException, status)

from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
import jwt
import logging
import uuid

async def system_logs(username, action):
    #generate UUID
    my_uuid = uuid.uuid4()

    logging.basicConfig(
        filename ='logging.log', 
        level=logging.INFO, 
        format="{} %(asctime)s {} {}".format(my_uuid, username, action), 
        datefmt = "%Y-%m-%d %H:%M:%S")
    
    logging.info(f"{my_uuid} {username} {action}")
