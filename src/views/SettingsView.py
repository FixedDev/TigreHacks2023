#Index View
import flet as ft
from flet import *

navbar = AppBar(
        title=ft.Text("EcoBalance"),
        actions=[
            ft.IconButton(ft.icons.ARROW_BACK_ROUNDED, on_click=lambda e: e.page.go('/index')),
            ft.IconButton(ft.icons.SETTINGS_ROUNDED, on_click=lambda e: e.page.go('/settings')),
        ]
    )

# avatar = ft.CircleAvatar(foreground_image_url="https://avatars.githubusercontent.com/u/68057133?v=4",
#                          radius=100)

logout = TextButton("Logout",on_click=lambda e: e.page.go('/login'))

def _view_():
    return View(
        '/settings',
        controls=[
            navbar,
            Text('Settings Page'),
            logout
        ],horizontal_alignment='center'
    )