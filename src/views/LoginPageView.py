#Login View
import flet as ft
from flet import *

def _view_():

    def login_handler(event):
        # Obtener el input del usuario
        entered_user_name = user_name.value
        entered_password = password.value

        # Realizar acciones con los valores ingresados
        print("Username:", entered_user_name)
        print("Password:", entered_password)

    singupBTN = ElevatedButton("Si no tienes cuenta, registrate aqui",
                               on_click=lambda e: e.page.go('/singup'),
                               bgcolor=colors.TRANSPARENT,
                               color=colors.WHITE)
    user_name = TextField(label='Username', value='', autofocus=True)
    password = TextField(label='Password', value='')
    loginBTN = ElevatedButton("Login",
                              on_click=lambda e: login_handler(e, user_name.value, password.value))

    def login_handler(e, user_name, password):
        print("Username login:", user_name)
        print("Password login:", password)
        e.page.go('/index')

    return View(
        '/login',
        controls=[
            singupBTN,
            user_name,
            password,
            loginBTN,
        ],
        horizontal_alignment='center',
        vertical_alignment='center'
    )