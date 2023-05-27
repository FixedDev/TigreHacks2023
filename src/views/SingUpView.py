#SingUp View
import flet as ft
from flet import *

def _view_():
    return View(
        '/singup',
        controls=[
            TextField(label='Username'),
            TextField(label='Password'),
            ElevatedButton("SingUp",
                            on_click=lambda e: e.page.go('/login')
                           ),
        ],
    )