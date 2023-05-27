#Index View
import flet as ft
from flet import *

def _view_():
    
    def enviar_otp():
        print("Enviando OTP")

    def singup_handler(e, otp_code):
        if otp_code == '':
            print('Ingrese datos!!!')
        else:
            print("OTP Code:", otp_code)
            e.page.go('/index')

    otp_code=TextField(label="Ingrese OTP")
    otpBTN = ElevatedButton("Enviar codigo", on_click=enviar_otp)
    sendBTN = ElevatedButton("Enviar", on_click=lambda e: singup_handler(e, otp_code.value))

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