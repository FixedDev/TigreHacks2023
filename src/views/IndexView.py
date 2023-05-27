#Index View
import flet as ft
from flet import *

navbar = AppBar(
        title=ft.Text("EcoBalance"),
        actions=[
            # ft.IconButton(ft.icons.HOME, on_click=lambda e: e.page.go('/index')),
            ft.IconButton(ft.icons.SETTINGS_ROUNDED, on_click=lambda e: e.page.go('/settings')),
        ]
    )

def _view_():
    return View(
        '/index',
        controls=[
            navbar,
            Text('Index Page')
        ],
    )