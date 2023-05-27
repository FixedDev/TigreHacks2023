#SingUp View
import flet as ft
from flet import *

def _view_():
    user_name = TextField(label='Username', value='')
    password = TextField(label='Password', value='')
    singupBTN = ElevatedButton("Sing Up", on_click=lambda e: singup_handler(e, user_name.value, password.value))

    def singup_handler(e, user_name, password):
        print("Username SingUp:", user_name)
        print("Password SingUp:", password)
        e.page.go('/login')


    return View(
        '/singup',
        controls=[
            user_name,
            password,
            singupBTN,
        ],
    )