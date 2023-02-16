import email
from fastapi import (BackgroundTasks, UploadFile, 
                    File, Form, Depends, HTTPException, status)

from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
import jwt


config_credentials = dict(dotenv_values(".env"))
conf = ConnectionConfig(
    MAIL_USERNAME = config_credentials["EMAIL"],
    MAIL_PASSWORD = config_credentials["PASS"],
    MAIL_FROM = config_credentials["EMAIL"],
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = False,
    MAIL_SSL = True,
    # MAIL_STARTTLS = False,
    # MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True
)

class EmailSchema(BaseModel):
    email: List[EmailStr] 

async def send_email(email : list, first, middle, last):

    register_template = f"""
    <!DOCTYPE html>

<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
<title></title>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
</head>
<body style="background-color: #283C4B; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<div class="spacer_block" style="height:20px;line-height:20px;font-size:1px;"> </div>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; padding-left: 15px; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="image_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;">
<div align="left" class="alignment" style="line-height:10px"><img alt="Image" src="https://faithhopeloveclinic.com/wp-content/uploads/2022/07/cropped-logo.png" style="display: block; height: auto; border: 0; width: 150px; padding: 10px; max-width: 100%;" title="Image" width="236"/></div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #8ECD81; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; padding-left: 10px; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:20px;padding-left:20px;padding-right:20px;padding-top:30px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #FFFFFF; line-height: 1.2;">
<p style="margin: 0; font-size: 18px; text-align: left; mso-line-height-alt: 21.599999999999998px;"><span style="font-size:24px;">Welcome to Faith Hope Love Clinic</span></p>
<p style="margin: 0; font-size: 18px; text-align: left; mso-line-height-alt: 21.599999999999998px;"><span style="font-size:24px;">Your password reset has been successful! </span><br/></p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 0px; padding-bottom: 10px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:5px;padding-left:30px;padding-right:30px;padding-top:25px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 18px; color: #283C4B; line-height: 1.5;">
<p style="margin: 0; font-size: 12px; mso-line-height-alt: 21px;"><span style="font-size:14px;">You may now book your appointment and buy our products using this account.</span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"></span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:20px;">Your New Account:</span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;">Name : {first} {middle} {last}</span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;">Email : {email[0]}</span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px; color:red">If you did not register for our clinic, please kindly ignore this email and nothing will happen. Thank you</span></p>
</div>
</div>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="button_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:10px;padding-top:10px;text-align:left;">
<div align="left" class="alignment">
<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="http://example.com" style="height:43px;width:122px;v-text-anchor:middle;" arcsize="0%" strokeweight="0.75pt" strokecolor="#85D874" fillcolor="#FFFFFF"><w:anchorlock/><v:textbox inset="0px,0px,0px,0px"><center style="color:#85D874; font-family:Arial, sans-serif; font-size:16px"><![endif]--><a href="http://127.0.0.1:8000/users/contact" style="text-decoration:none;display:inline-block;color:#85D874;background-color:#FFFFFF;border-radius:0px;width:auto;border-top:1px solid #85D874;font-weight:undefined;border-right:1px solid #85D874;border-bottom:1px solid #85D874;border-left:1px solid #85D874;padding-top:5px;padding-bottom:5px;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-size:16px;text-align:center;mso-border-alt:none;word-break:keep-all;" target="_blank"><span style="padding-left:20px;padding-right:20px;font-size:16px;display:inline-block;letter-spacing:normal;"><span style="word-break: break-word; line-height: 32px;">Contact Us</span></span></a>
<!--[if mso]></center></v:textbox></v:roundrect><![endif]-->
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-5" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #F6F6F6; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="33.333333333333336%">
<table border="0" cellpadding="0" cellspacing="0" class="image_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;padding-top:5px;">
<div align="center" class="alignment" style="line-height:10px"><img alt="Image" src="https://faithhopeloveclinic.com/wp-content/uploads/2022/07/Dra.jpg" style="display: block; height: auto; border: 0; width: 200px; max-width: 100%;" title="Image" width="200"/></div>
</td>
</tr>
</table>
</td>
<td class="column column-2" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="66.66666666666667%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:10px;padding-top:25px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #85D874; line-height: 1.2;">
<p style="margin: 0; font-size: 14px; mso-line-height-alt: 16.8px;">DR. LEE</p>
</div>
</div>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:5px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 18px; color: #283C4B; line-height: 1.5;">
<p style="margin: 0; font-size: 12px; mso-line-height-alt: 19.5px;"><span style="font-size:13px;">Dr. Lee of Faith Hope Love Medical Center has practiced traditional Chinese Medicine in the Philippines for 40 years and still continues to serve patients to this day.</span></p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-6" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="25" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #555555; line-height: 1.2;">
<p style="margin: 0; font-size: 14px; text-align: left; mso-line-height-alt: 16.8px;">Copyright @ Faith Hope Love Medical Clinic</p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-7" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<div class="spacer_block" style="height:30px;line-height:30px;font-size:1px;"> </div>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-8" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="icons_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="vertical-align: middle; color: #9d9d9d; font-family: inherit; font-size: 15px; padding-bottom: 5px; padding-top: 5px; text-align: center;">
<table cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="alignment" style="vertical-align: middle; text-align: center;">
<!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
<!--[if !vml]><!-->
<table cellpadding="0" cellspacing="0" class="icons-inner" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block; margin-right: -4px; padding-left: 0px; padding-right: 0px;">
<!--<![endif]-->
<tr>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table><!-- End -->
</body>
</html>
        
    """

    message = MessageSchema(
        subject="Faith, Hope, Love Clinic Account Registration",
        recipients=email,  # List of recipients, as many as you can pass 
        html=register_template,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message) 
  
async def send_appointment(email : list, user, ddate, startt, endt, service, amount):

    register_template = f"""<!DOCTYPE html>

<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
<title></title>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
</head>
<body style="background-color: #283C4B; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<div class="spacer_block" style="height:20px;line-height:20px;font-size:1px;"> </div>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; padding-left: 15px; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="image_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;">
<div align="left" class="alignment" style="line-height:10px"><img alt="Image" src="https://faithhopeloveclinic.com/wp-content/uploads/2022/07/cropped-logo.png" style="display: block; height: auto; border: 0; width: 150px; padding: 10px; max-width: 100%;" title="Image" width="236"/></div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #8ECD81; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; padding-left: 10px; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:20px;padding-left:20px;padding-right:20px;padding-top:30px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #FFFFFF; line-height: 1.2;">
<p style="margin: 0; font-size: 18px; text-align: left; mso-line-height-alt: 21.599999999999998px;"><span style="font-size:24px;">Hello { user },</span></p>
<p style="margin: 0; font-size: 18px; text-align: left; mso-line-height-alt: 21.599999999999998px;"><span style="font-size:24px;">This is our appointment confirmation! </span><br/></p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 0px; padding-bottom: 10px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:5px;padding-left:30px;padding-right:30px;padding-top:25px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 18px; color: #283C4B; line-height: 1.5;">
<p style="margin: 0; font-size: 12px; mso-line-height-alt: 21px;"><span style="font-size:14px;">We look forward to welcoming you to our clinic on {ddate} at {startt} - {endt}.</span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;">Our professional and friendly staff are committed to ensuring your visit is both enjoyable and comfortable.</span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;">Should you have any requests prior to your stay, please do not hesitate to contact us and we will endeavor to assist you whenever possible.</span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;">Please prepare the exact amount of {amount}₱ for availing the service of {service}. Thank you.</span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;">Thanks & Best Regards</span></p>
</div>
</div>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="button_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:10px;padding-top:10px;text-align:left;">
<div align="left" class="alignment">
<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="http://example.com" style="height:43px;width:122px;v-text-anchor:middle;" arcsize="0%" strokeweight="0.75pt" strokecolor="#85D874" fillcolor="#FFFFFF"><w:anchorlock/><v:textbox inset="0px,0px,0px,0px"><center style="color:#85D874; font-family:Arial, sans-serif; font-size:16px"><![endif]--><a href="http://127.0.0.1:8000/users/contact" style="text-decoration:none;display:inline-block;color:#85D874;background-color:#FFFFFF;border-radius:0px;width:auto;border-top:1px solid #85D874;font-weight:undefined;border-right:1px solid #85D874;border-bottom:1px solid #85D874;border-left:1px solid #85D874;padding-top:5px;padding-bottom:5px;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-size:16px;text-align:center;mso-border-alt:none;word-break:keep-all;" target="_blank"><span style="padding-left:20px;padding-right:20px;font-size:16px;display:inline-block;letter-spacing:normal;"><span style="word-break: break-word; line-height: 32px;">Contact Us</span></span></a>
<!--[if mso]></center></v:textbox></v:roundrect><![endif]-->
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-5" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #F6F6F6; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="33.333333333333336%">
<table border="0" cellpadding="0" cellspacing="0" class="image_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;padding-top:5px;">
<div align="center" class="alignment" style="line-height:10px"><img alt="Image" src="https://faithhopeloveclinic.com/wp-content/uploads/2022/07/Dra.jpg" style="display: block; height: auto; border: 0; width: 200px; max-width: 100%;" title="Image" width="200"/></div>
</td>
</tr>
</table>
</td>
<td class="column column-2" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="66.66666666666667%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:10px;padding-top:25px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #85D874; line-height: 1.2;">
<p style="margin: 0; font-size: 14px; mso-line-height-alt: 16.8px;">DR. LEE</p>
</div>
</div>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:5px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 18px; color: #283C4B; line-height: 1.5;">
<p style="margin: 0; font-size: 12px; mso-line-height-alt: 19.5px;"><span style="font-size:13px;">Dr. Lee of Faith Hope Love Medical Center has practiced traditional Chinese Medicine in the Philippines for 40 years and still continues to serve patients to this day.</span></p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-6" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="25" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #555555; line-height: 1.2;">
<p style="margin: 0; font-size: 14px; text-align: left; mso-line-height-alt: 16.8px;">Copyright @ Faith Hope Love Medical Clinic</p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-7" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<div class="spacer_block" style="height:30px;line-height:30px;font-size:1px;"> </div>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-8" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="icons_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="vertical-align: middle; color: #9d9d9d; font-family: inherit; font-size: 15px; padding-bottom: 5px; padding-top: 5px; text-align: center;">
<table cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="alignment" style="vertical-align: middle; text-align: center;">
<!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
<!--[if !vml]><!-->
<table cellpadding="0" cellspacing="0" class="icons-inner" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block; margin-right: -4px; padding-left: 0px; padding-right: 0px;">
<!--<![endif]-->
<tr>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table><!-- End -->
</body>
</html>
    """

    message = MessageSchema(
        subject="Faith, Hope, Love Clinic Appointment Notification",
        recipients=email,  # List of recipients, as many as you can pass 
        html=register_template,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)

async def for_pickup(email: list):

    register_template = f"""<!DOCTYPE html>

<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
<title></title>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
</head>
<body style="background-color: #283C4B; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<div class="spacer_block" style="height:20px;line-height:20px;font-size:1px;"> </div>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; padding-left: 15px; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="image_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;">
<div align="left" class="alignment" style="line-height:10px"><img alt="Image" src="https://faithhopeloveclinic.com/wp-content/uploads/2022/07/cropped-logo.png" style="display: block; height: auto; border: 0; width: 150px; padding: 10px; max-width: 100%;" title="Image" width="236"/></div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #8ECD81; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; padding-left: 10px; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:20px;padding-left:20px;padding-right:20px;padding-top:30px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #FFFFFF; line-height: 1.2;">
<p style="margin: 0; font-size: 18px; text-align: left; mso-line-height-alt: 21.599999999999998px;"><span style="font-size:24px;">Welcome to Faith Hope Love Clinic</span></p>
<p style="margin: 0; font-size: 18px; text-align: left; mso-line-height-alt: 21.599999999999998px;"><span style="font-size:24px;">This is our order notification! </span><br/></p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 0px; padding-bottom: 10px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:5px;padding-left:30px;padding-right:30px;padding-top:25px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 18px; color: #283C4B; line-height: 1.5;">
<p style="margin: 0; font-size: 12px; mso-line-height-alt: 21px;"><span style="font-size:14px;"></span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"></span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:20px;">Order Complete!</span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;">You may now check your account and visit our store to pick-up your orders!</span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"></span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px; color:red"></span></p>
</div>
</div>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="button_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:10px;padding-top:10px;text-align:left;">
<div align="left" class="alignment">
<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="http://example.com" style="height:43px;width:122px;v-text-anchor:middle;" arcsize="0%" strokeweight="0.75pt" strokecolor="#85D874" fillcolor="#FFFFFF"><w:anchorlock/><v:textbox inset="0px,0px,0px,0px"><center style="color:#85D874; font-family:Arial, sans-serif; font-size:16px"><![endif]--><a href="http://127.0.0.1:8000/users/login" style="text-decoration:none;display:inline-block;color:#85D874;background-color:#FFFFFF;border-radius:0px;width:auto;border-top:1px solid #85D874;font-weight:undefined;border-right:1px solid #85D874;border-bottom:1px solid #85D874;border-left:1px solid #85D874;padding-top:5px;padding-bottom:5px;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-size:16px;text-align:center;mso-border-alt:none;word-break:keep-all;" target="_blank"><span style="padding-left:20px;padding-right:20px;font-size:16px;display:inline-block;letter-spacing:normal;"><span style="word-break: break-word; line-height: 32px;">Log-in Here</span></span></a>
<!--[if mso]></center></v:textbox></v:roundrect><![endif]-->
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-5" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #F6F6F6; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="33.333333333333336%">
<table border="0" cellpadding="0" cellspacing="0" class="image_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;padding-top:5px;">
<div align="center" class="alignment" style="line-height:10px"><img alt="Image" src="https://faithhopeloveclinic.com/wp-content/uploads/2022/07/Dra.jpg" style="display: block; height: auto; border: 0; width: 200px; max-width: 100%;" title="Image" width="200"/></div>
</td>
</tr>
</table>
</td>
<td class="column column-2" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="66.66666666666667%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:10px;padding-top:25px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #85D874; line-height: 1.2;">
<p style="margin: 0; font-size: 14px; mso-line-height-alt: 16.8px;">DR. LEE</p>
</div>
</div>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:5px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 18px; color: #283C4B; line-height: 1.5;">
<p style="margin: 0; font-size: 12px; mso-line-height-alt: 19.5px;"><span style="font-size:13px;">Dr. Lee of Faith Hope Love Medical Center has practiced traditional Chinese Medicine in the Philippines for 40 years and still continues to serve patients to this day.</span></p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-6" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="25" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #555555; line-height: 1.2;">
<p style="margin: 0; font-size: 14px; text-align: left; mso-line-height-alt: 16.8px;">Copyright @ Faith Hope Love Medical Clinic</p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-7" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<div class="spacer_block" style="height:30px;line-height:30px;font-size:1px;"> </div>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-8" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="icons_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="vertical-align: middle; color: #9d9d9d; font-family: inherit; font-size: 15px; padding-bottom: 5px; padding-top: 5px; text-align: center;">
<table cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="alignment" style="vertical-align: middle; text-align: center;">
<!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
<!--[if !vml]><!-->
<table cellpadding="0" cellspacing="0" class="icons-inner" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block; margin-right: -4px; padding-left: 0px; padding-right: 0px;">
<!--<![endif]-->
<tr>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table><!-- End -->
</body>
</html>    """

    message = MessageSchema(
        subject="Faith, Hope, Love Clinic Order Notification",
        recipients=email,  # List of recipients, as many as you can pass 
        html=register_template,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)

async def passwordChange(email: list, newPassword):

    register_template = f"""<!DOCTYPE html>

<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
<title></title>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
</head>
<body style="background-color: #283C4B; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
<table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<div class="spacer_block" style="height:20px;line-height:20px;font-size:1px;"> </div>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; padding-left: 15px; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="image_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;">
<div align="left" class="alignment" style="line-height:10px"><img alt="Image" src="https://faithhopeloveclinic.com/wp-content/uploads/2022/07/cropped-logo.png" style="display: block; height: auto; border: 0; width: 150px; padding: 10px; max-width: 100%;" title="Image" width="236"/></div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #8ECD81; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; padding-left: 10px; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:20px;padding-left:20px;padding-right:20px;padding-top:30px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #FFFFFF; line-height: 1.2;">
<p style="margin: 0; font-size: 18px; text-align: left; mso-line-height-alt: 21.599999999999998px;"><span style="font-size:24px;">Welcome to Faith Hope Love Clinic</span></p>
<p style="margin: 0; font-size: 18px; text-align: left; mso-line-height-alt: 21.599999999999998px;"><span style="font-size:24px;">Your registration is completed! </span><br/></p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-4" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #283C4B;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 0px; padding-bottom: 10px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:5px;padding-left:30px;padding-right:30px;padding-top:25px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 18px; color: #283C4B; line-height: 1.5;">
<p style="margin: 0; font-size: 12px; mso-line-height-alt: 21px;"><span style="font-size:14px;">You may now log-in using this password to our clinic.</span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"></span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:20px;">Your New Account:</span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;">Email : {email[0]}</span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;">Your new password : {newPassword}</span></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px;"> </span><br/></p>
<p style="margin: 0; font-size: 12px; text-align: left; mso-line-height-alt: 21px;"><span style="font-size:14px; color:red">If you did not change your password, kindly be alert towards potential suspicious activity in your account.</span></p>
</div>
</div>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="button_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:10px;padding-top:10px;text-align:left;">
<div align="left" class="alignment">
<!--[if mso]><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="http://example.com" style="height:43px;width:122px;v-text-anchor:middle;" arcsize="0%" strokeweight="0.75pt" strokecolor="#85D874" fillcolor="#FFFFFF"><w:anchorlock/><v:textbox inset="0px,0px,0px,0px"><center style="color:#85D874; font-family:Arial, sans-serif; font-size:16px"><![endif]--><a href="http://127.0.0.1:8000/users/contact" style="text-decoration:none;display:inline-block;color:#85D874;background-color:#FFFFFF;border-radius:0px;width:auto;border-top:1px solid #85D874;font-weight:undefined;border-right:1px solid #85D874;border-bottom:1px solid #85D874;border-left:1px solid #85D874;padding-top:5px;padding-bottom:5px;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-size:16px;text-align:center;mso-border-alt:none;word-break:keep-all;" target="_blank"><span style="padding-left:20px;padding-right:20px;font-size:16px;display:inline-block;letter-spacing:normal;"><span style="word-break: break-word; line-height: 32px;">Contact Us</span></span></a>
<!--[if mso]></center></v:textbox></v:roundrect><![endif]-->
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-5" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #F6F6F6; color: #333; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="33.333333333333336%">
<table border="0" cellpadding="0" cellspacing="0" class="image_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="width:100%;padding-right:0px;padding-left:0px;padding-top:5px;">
<div align="center" class="alignment" style="line-height:10px"><img alt="Image" src="https://faithhopeloveclinic.com/wp-content/uploads/2022/07/Dra.jpg" style="display: block; height: auto; border: 0; width: 200px; max-width: 100%;" title="Image" width="200"/></div>
</td>
</tr>
</table>
</td>
<td class="column column-2" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="66.66666666666667%">
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:10px;padding-top:25px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #85D874; line-height: 1.2;">
<p style="margin: 0; font-size: 14px; mso-line-height-alt: 16.8px;">DR. LEE</p>
</div>
</div>
</td>
</tr>
</table>
<table border="0" cellpadding="0" cellspacing="0" class="text_block block-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad" style="padding-bottom:10px;padding-left:30px;padding-right:30px;padding-top:5px;">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 18px; color: #283C4B; line-height: 1.5;">
<p style="margin: 0; font-size: 12px; mso-line-height-alt: 19.5px;"><span style="font-size:13px;">Dr. Lee of Faith Hope Love Medical Center has practiced traditional Chinese Medicine in the Philippines for 40 years and still continues to serve patients to this day.</span></p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-6" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="25" cellspacing="0" class="text_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
<tr>
<td class="pad">
<div style="font-family: sans-serif">
<div class="" style="font-size: 12px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 14.399999999999999px; color: #555555; line-height: 1.2;">
<p style="margin: 0; font-size: 14px; text-align: left; mso-line-height-alt: 16.8px;">Copyright @ Faith Hope Love Medical Clinic</p>
</div>
</div>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-7" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 0px; padding-bottom: 0px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<div class="spacer_block" style="height:30px;line-height:30px;font-size:1px;"> </div>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-8" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tbody>
<tr>
<td>
<table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 600px;" width="600">
<tbody>
<tr>
<td class="column column-1" style="text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;" width="100%">
<table border="0" cellpadding="0" cellspacing="0" class="icons_block block-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="pad" style="vertical-align: middle; color: #9d9d9d; font-family: inherit; font-size: 15px; padding-bottom: 5px; padding-top: 5px; text-align: center;">
<table cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
<tr>
<td class="alignment" style="vertical-align: middle; text-align: center;">
<!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
<!--[if !vml]><!-->
<table cellpadding="0" cellspacing="0" class="icons-inner" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; display: inline-block; margin-right: -4px; padding-left: 0px; padding-right: 0px;">
<!--<![endif]-->
<tr>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table><!-- End -->
</body>
</html>"""

    message = MessageSchema(
        subject="Faith, Hope, Love Clinic Password Reset Notification",
        recipients=email,  # List of recipients, as many as you can pass 
        html=register_template,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)


