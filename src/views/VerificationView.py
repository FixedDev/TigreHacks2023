#Index View
import flet as ft
from flet import *
from twilio.rest import Client
from ..views.SingUpView import get_phone_number

phoneNumber = get_phone_number().value
account_sid = "AC71fe53ec2dfed522c750de17b5fcdbaf"
auth_token = "2de456c412533d905b2e76fcc8f5c935"
verify_sid = "VAbd25cf8f908bd1c0619dfeca506ccfb1"
client = Client(account_sid, auth_token)

def _view_():
    def enviarOtp(e):
        print("Enviando OTP a ",phoneNumber)
        verified_number = f"{phoneNumber}"

        verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=verified_number, channel="sms")
        print(verification.status)
        
        #esto hay que moverlo
        otp_code = otp_code

        verification_check = client.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=verified_number, code=otp_code)
        print(verification_check.status)


    def send_handler(e, otp_code):
        if otp_code == '':
            print('Ingrese datos!!!')
        else:
            e.page.go('/index')
            print('OTP Code Correct!!!')
    
    otp_code=TextField(label="Ingrese OTP")
    otpBTN = ElevatedButton("Enviar codigo", on_click=enviarOtp)
    sendBTN = ElevatedButton("Enviar", on_click=lambda e: send_handler(e, otp_code.value))

    return View(
        '/verification',
        controls=[
            Text('Verification Page'),
            Row(controls=[
                otp_code, 
                otpBTN]),
            sendBTN
        ],
    )