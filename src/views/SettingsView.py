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

# avatar = ft.CircleAvatar(foreground_image_url="https://avatars.githubusercontent.com/u/wilovy09?v=4",
#                          radius=100)
avatar = ft.CircleAvatar(foreground_image_url="https://avatars.githubusercontent.com/u/68057133?v=4",
                         radius=100)

def _view_():
    return View(
        '/settings',
        controls=[
            navbar,
            avatar,
            Text('Settings Page')
        ],horizontal_alignment='center'
    )