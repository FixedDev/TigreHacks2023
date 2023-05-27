#SingUp View
import flet as ft
from flet import *

def _view_():
    phoneNumber = TextField(label='Phone number', value='')
    password = TextField(label='Password', value='')
    singupBTN = ElevatedButton("Sing Up", on_click=lambda e: singup_handler(e, phoneNumber.value, password.value))

    def singup_handler(e, phoneNumber, password):
        print("Username SingUp:", phoneNumber)
        print("Password SingUp:", password)
        e.page.go('/login')

    return View(
        '/singup',
        controls=[
            phoneNumber,
            password,
            singupBTN,
        ],
    )