#Login View
import flet as ft
from flet import *

def _view_():
    return View(
        '/login',
        controls=[
            ElevatedButton("Si no tienes cuenta, registrate aqui",
                           on_click=lambda e: e.page.go('/singup'),
                           ),
            TextField(label='Username'),
            TextField(label='Password'),
            ElevatedButton("Login",
                           on_click=lambda e: e.page.go('/index'),
                           ),
        ],
    )