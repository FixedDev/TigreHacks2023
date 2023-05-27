#Index View
import flet as ft
from flet import *

def _view_():
    navbar = AppBar(
            title=ft.Text("EcoBalance"),
            actions=[
                ft.IconButton(ft.icons.ARROW_BACK_ROUNDED, on_click=lambda e: e.page.go('/index')),
                ft.IconButton(ft.icons.SETTINGS_ROUNDED, on_click=lambda e: e.page.go('/settings')),
            ]
        )

    # avatar = ft.CircleAvatar(foreground_image_url="https://avatars.githubusercontent.com/u/68057133?v=4",
    #                          radius=100)

    img = ft.Image(src=f'TigreHacks2023/assets/img/telcel.png')
    logout = TextButton("Logout",on_click=lambda e: e.page.go('/login'))

    return View(
        '/settings',
        controls=[
            navbar,
            Text('Settings Page'),
            img,
            logout
        ],horizontal_alignment='center'
    )