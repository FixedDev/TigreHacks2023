import flet as ft
from flet import *
from src.views.LoginPageView import _view_ as LoginPage
from src.views.SingUpView import _view_ as SingUpPage
from src.views.IndexView import _view_ as IndexPage

def main(page:Page):
    print("Welcome to TigreHacks 2023")
    page.theme_mode = "dark"

    def route_change(route):
        page.views.clear()
        if page.route == '/login':
            page.views.append(LoginPage())
        if page.route == '/singup':
            page.views.append(SingUpPage())
        if page.route == '/index':
            page.views.append(IndexPage())
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    page.views.append(IndexPage())
    page.views.append(SingUpPage())
    page.views.append(LoginPage())
    
    page.update()
    

ft.app(target=main)