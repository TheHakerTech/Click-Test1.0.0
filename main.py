import flet as ft
from pages.clicker import init_clicker
from pages.history import init_history

def main(page: ft.Page):
    def change(e: ft.ControlEvent):
        page.controls = []
        page.update()

        match e.control.selected_index:
            case 0:
                init_clicker(page)
                page.update()
            case 1:
                init_history(page)
                page.update()

    page.navigation_bar = ft.NavigationBar(
        on_change=change,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.MOUSE_OUTLINED, selected_icon=ft.icons.MOUSE, label='Click'),
            ft.NavigationDestination(icon=ft.icons.HISTORY, label='History')
        ]
    )

    init_clicker(page)
    page.update()

ft.app(main)