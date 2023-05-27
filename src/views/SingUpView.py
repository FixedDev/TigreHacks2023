#SingUp View
import flet as ft
from flet import *

def _view_():
    phoneNumber = TextField(label='Phone number', value='', )
    password = TextField(label='Password', value='')
    verificationBTN = ElevatedButton("Sing Up", on_click=lambda e: singup_handler(e, phoneNumber.value, password.value))
    
    def singup_handler(e, phoneNumber, password):
        if phoneNumber == '' or password == '':
            print('Ingrese datos!!!')
        else:
            print("Number SingUp:", phoneNumber)
            print("Password SingUp:", password)
            e.page.go('/verification')

    return View(
        '/singup',
        controls=[
            phoneNumber,
            password,
            verificationBTN,
        ],
        horizontal_alignment='center',
        vertical_alignment='center'
    )